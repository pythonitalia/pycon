FROM python:3.6.4@sha256:e5a05b8979f5cd1d43433a75663ed9a9d04227a3473c89abfe60b027ca334256

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
COPY requirements.txt /app/
COPY requirements/ /app/requirements/
RUN pip3 install --no-cache-dir -r requirements.txt

# -- Install dependencies:
COPY . /app/

# # uWSGI will listen on this port
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

# # uWSGI configuration (customize as needed):
ENV UWSGI_WSGI_FILE=pycon/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=3
ENV UWSGI_THREADS=10 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# # Start uWSGI
CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive", "--static-map", "/admin-static=/app/assets"]