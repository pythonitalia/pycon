from invoke import task


@task
def makemigrations(c, name):
    c.run(f'alembic revision --autogenerate -m "{name}"')


@task
def migrate(c):
    c.run("alembic upgrade head")


@task
def server(c):
    c.run("uvicorn main:app --reload")
