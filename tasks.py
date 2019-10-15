from invoke import task
from invoke.exceptions import Failure
from invoke.tasks import call


def run_or_fail(c, cmd, fail_message="Error", fail_callback=None):
    try:
        cmd(c)
    except Failure as ex:
        print(fail_message)
        if fail_callback:
            fail_callback(c)
        exit()

@task()
def tools_check(c, tools=[]):
    missing_tools = []
    for tool in tools:
        if c.run(f"which {tool}", hide=True, warn=True).exited != 0:
            missing_tools.append(f"{tool}")

    if len(missing_tools) > 0:
        print("These tools are required : {}".format(", ".join(missing_tools)))
        print("Please install them")
        exit()


@task(pre=[call(tools_check, ["yarn"])])
def setup_frontend(c):
    print("Running frontend setup...")

    with c.cd("frontend"):
        c.run("yarn")


@task(pre=[call(tools_check, ["docker"])])
def setup_db(c):
    print("Running DB setup...")

    with c.cd("backend"):
        run_or_fail(c, lambda x: x.run("ls .env", hide=True),
                    fail_message="ERROR! Please copy backend/.env.sample "
                                 "in backend/.env and set your .env vars")
        with c.prefix(". .env"):
            run_or_fail(c, lambda x: x.run("docker info", hide=True),
                        fail_message="ERROR! Is Docker running?")
            run_or_fail(c, lambda x: x.run("docker volume create s$DOCKER_DB_VOLUME", hide=True),
                        fail_message=f"ERROR! Docker volume '$DOCKER_DB_VOLUME' has not "
                                     f"been created\n"
                                     f"Here the results of command 'docker volume inspect $DOCKER_DB_VOLUME'",
                        fail_callback=lambda x: x.run("docker volume inspect $DOCKER_DB_VOLUME"))
            run_or_fail(c, lambda x: x.run("docker start $DOCKER_DB_CONTAINER ||"
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
                                           " postgres:11", hide=True),
                        fail_message=f"ERROR! Something went wrong with launching "
                                     f"'docker run'")

    print("... DB setup completed!")


@task(pre=[call(tools_check, ["poetry"])])
def setup_backend(c):
    print("Running backend setup...")

    with c.cd("backend"):
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
        c.run("poetry run python manage.py createsuperuser", pty=True)


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
