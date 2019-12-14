FROM python:3.7

RUN set -ex && mkdir /app

WORKDIR /app

RUN pip3 install poetry
COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app/

RUN mkdir /app/assets

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN SLACK_INCOMING_WEBHOOK_URL=example \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    python manage.py collectstatic --noinput

ENV UWSGI_WSGI_FILE=pycon/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=3
ENV UWSGI_THREADS=10 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]
