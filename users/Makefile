makemigrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

server:
	poetry run uvicorn main:app --reload
