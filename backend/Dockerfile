ARG FUNCTION_DIR="/home/app/"

FROM python:3.9-alpine as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apk add build-base jpeg-dev zlib-dev libxml2-dev libxslt-dev postgresql-libs make cmake libtool \
    autoconf \
    libexecinfo-dev \
    libcurl \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo

RUN apk add --no-cache --virtual .build-deps postgresql-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip3 install poetry

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN apk add automake git

RUN pip3 install awslambdaric

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM python:3.9-alpine

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /usr/lib/libpq* \
    /usr/lib/libpq* \
    /usr/lib/libldap_r* \
    /usr/lib/liblber* \
    /usr/lib/libsasl* \
    /usr/lib/libxslt* \
    /usr/lib/libexslt* \
    /usr/lib/libxml2* \
    /usr/lib/libgcrypt* \
    /usr/lib/libgpg-error* \
    /usr/lib/libstdc++* \
    /usr/lib/libgcc_s* \
    /usr/lib/libjpeg* \
    /usr/lib/

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN USERS_SERVICE=empty \
    ASSOCIATION_BACKEND_SERVICE=empty \
    SERVICE_TO_SERVICE_SECRET=empty \
    SLACK_INCOMING_WEBHOOK_URL=example \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    PASTAPORTO_SECRET=demo \
    python manage.py collectstatic --noinput

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
