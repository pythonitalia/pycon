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
        else:
            exit()


@task()
def init_env(c):
    with c.cd("backend"):
        if not c.run("[ -f \".env\" ]", hide=False, warn=True):
            c.run("cp .env.sample .env")
            print(".env correctly initialized")
        else:
            print(".env already initialized")


@task()
def check_env_preconditions(c, env_vars=[]):
    """
    env_vars is an array of env variables you want to check
    """
    with c.cd("backend"):
        run_or_fail(c, lambda x: x.run("[ -f \".env\" ]", hide=False),
                    fail_message="ERROR! .env not configured."
                                 "Launch 'invoke init-env'")
        with c.prefix(". .env"):
            _env_check_failed = False
            for env_var in env_vars:
                if c.run(f"[ -z \"${env_var}\" ]", hide=True, warn=True):
                    print(f".env var {env_var} is required")
                    _env_check_failed = True
            if _env_check_failed:
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


@task(pre=[call(tools_check, ["docker", "docker-compose"]),
           call(check_env_preconditions, [])])
def setup_db(c):
    print("Running DB setup...")
    with c.cd("backend"):
        with c.prefix(". .env"):
            run_or_fail(c, lambda x: x.run("docker-compose -f docker-compose_dev.yml up", hide=False),
                        fail_message="ERROR! Some problem with docker-compose")

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
