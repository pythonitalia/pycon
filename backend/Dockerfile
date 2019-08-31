FROM python:3.7

RUN set -ex && mkdir /app

WORKDIR /app

COPY requirements.txt /app/
COPY requirements/ /app/requirements/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir /app/assets

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN AWS_MEDIA_BUCKET=example SECRET_KEY=DEMO python manage.py collectstatic --noinput

ENV UWSGI_WSGI_FILE=pycon/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=3
ENV UWSGI_THREADS=10 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]
