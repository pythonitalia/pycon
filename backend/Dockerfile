ARG FUNCTION_DIR="/home/app/"

FROM python:3.9-slim as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apt-get update -y && apt-get install -y gcc \
    libpq-dev \
    git \
    libtiff5-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev

ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip3 install poetry==1.1.13

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN pip3 install awslambdaric

RUN poetry config virtualenvs.path /venv
RUN poetry install --no-dev

FROM python:3.9-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage /venv /venv

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
    CFP_SLACK_INCOMING_WEBHOOK_URL=example \
    SUBMISSION_COMMENT_SLACK_INCOMING_WEBHOOK_URL=example \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    PASTAPORTO_SECRET=demo \
    /venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/venv/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
