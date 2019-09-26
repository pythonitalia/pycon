from invoke import task


@task()
def setup_frontend(c):
    print("Running frontend setup...")

    with c.cd("frontend"):
        c.run("yarn")


@task()
def setup_backend(c):
    print("Running backend setup...")

    with c.cd("backend"):
        c.run("poetry install", pty=True)


@task(setup_frontend, setup_backend)
def setup(c):
    print("Setup completed!")


@task()
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
