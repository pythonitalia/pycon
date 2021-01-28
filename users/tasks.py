from invoke import task


@task
def makemigrations(c, name):
    c.run(f'alembic revision --autogenerate -m "{name}"', pty=True)


@task
def migrate(c):
    c.run("alembic upgrade head", pty=True)


@task
def server(c):
    c.run("uvicorn main:app --reload", pty=True)
