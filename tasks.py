from invoke import task
from invoke.exceptions import Failure

@task()
def setup_frontend(c):
    print("Running frontend setup...")

    with c.cd("frontend"):
        c.run("yarn")


@task()
def setup_db(c):
    print("Running DB setup...")

    with c.cd("backend"):
        try:
            c.run("cat .env", hide=True)
        except Failure as ex:
            print("ERROR! Please copy backend/.env.sample in backend/.env and set your "
                  ".env vars")
            raise ex
        else:
            with c.prefix("source .env"):
                try:
                    c.run("docker -v", hide=True)
                except Failure as ex:
                    print("ERROR! Is Docker installed?")
                    raise ex
                else:
                    try:
                        c.run("docker info", hide=True)
                    except Failure as ex:
                        print("ERROR! Is Docker running?")
                        raise ex
                    else:
                        try:
                            c.run("docker volume create $DOCKER_DB_VOLUME", hide=True)
                        except Failure as ex:
                            print(f"ERROR! Docker volume '$DOCKER_DB_VOLUME' has not "
                                  f"been created:")
                            print(f"Here the results of command 'docker volume inspect "
                                  f"$DOCKER_DB_VOLUME':")
                            c.run("docker volume inspect $DOCKER_DB_VOLUME")
                            raise ex
                        else:
                            try:
                                c.run("docker start $DOCKER_DB_CONTAINER ||"
                                      " docker run"
                                      " --name=$DOCKER_DB_CONTAINER"
                                      " -d"
                                      " -e POSTGRES_USER=$DB_USER"
                                      " -e POSTGRES_PASSWORD=$DB_PASSWORD"
                                      " -e POSTGRES_DB=$DB_NAME"
                                      " -e ALLOW_IP_RANGE=0.0.0.0/0"
                                      " -p $DB_PORT:$DOCKER_DB_PORT"
                                      " -v $DOCKER_DB_VOLUME:/var/lib/postgresql"
                                      " --restart=always"
                                      " postgres:11", hide=True)
                            except Failure as ex:
                                print(f"ERROR! Something went wrong with launching "
                                      f"'docker run'")
                                raise ex

    print("... DB setup completed!")


@task()
def setup_backend(c):
    print("Running backend setup...")

    with c.cd("backend"):
        c.run("pip install poetry", hide=True, warn=True)
        c.run("poetry install", pty=True)

    print("... backend setup completed!")


@task(setup_frontend, setup_backend)
def setup(c):
    print("Setup completed!")


@task(setup_db)
def migrate(c):
    with c.cd("backend"):
        c.run("poetry run python manage.py migrate")


@task(migrate)
def demo_data(c):
    print("Loading demo data")

    with c.cd("backend"):
        c.run("poetry run python manage.py loaddata demodata/*.json")
        c.run("cp -r demodata/media media")


@task(migrate)
def createsuperuser(c):
    with c.cd("backend"):
        c.run("poetry run python manage.py createsuperuser")


@task(migrate)
def run_backend(c):
    with c.cd("backend"):
        c.run("poetry run python manage.py runserver", pty=True)


@task(setup_frontend)
def run_frontend(c):
    with c.cd("frontend"):
        c.run("yarn start")


@task(setup_frontend)
def build(c):
    with c.cd("frontend"):
        c.run("yarn build")


@task(setup_frontend)
def build_styleguide(c):
    with c.cd("frontend"):
        c.run("yarn build:docz")
