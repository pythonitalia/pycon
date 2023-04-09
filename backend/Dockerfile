ARG FUNCTION_DIR="/home/app/"

FROM node:18.12.1 as js-stage

ARG FUNCTION_DIR
ARG GRAPHQL_SCHEMA_URL

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN npm install -g pnpm

COPY custom_admin/js/package.json custom_admin/js/pnpm-lock.yaml ./

RUN pnpm install

COPY custom_admin/js/ .

ENV GRAPHQL_SCHEMA_URL ${GRAPHQL_SCHEMA_URL}

RUN pnpm codegen && pnpm build

FROM python:3.9-slim as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apt-get update -y && apt-get install -y \
    gcc libpq-dev git \
    # Pillow
    libtiff5-dev libjpeg62 libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

ENV LIBRARY_PATH=/lib:/usr/lib

RUN tar -czvf /libs.tar.gz /usr/lib/x86_64-linux-gnu/libpq* \
    /usr/lib/x86_64-linux-gnu/libpq* \
    /usr/lib/x86_64-linux-gnu/libldap_r* \
    /usr/lib/x86_64-linux-gnu/liblber* \
    /usr/lib/x86_64-linux-gnu/libsasl* \
    /usr/lib/x86_64-linux-gnu/libxml2* \
    /usr/lib/x86_64-linux-gnu/libgcrypt* \
    /usr/lib/x86_64-linux-gnu/libstdc++* \
    /usr/lib/x86_64-linux-gnu/libjpeg* \
    /usr/lib/x86_64-linux-gnu/libopenjp2* \
    /usr/lib/x86_64-linux-gnu/libdeflate* \
    /usr/lib/x86_64-linux-gnu/libjbig* \
    /usr/lib/x86_64-linux-gnu/liblcms2* \
    /usr/lib/x86_64-linux-gnu/libwebp* \
    /usr/lib/x86_64-linux-gnu/libtiff*

RUN pip3 install poetry==1.3.2

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev -E lambda

FROM python:3.9-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv
COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /libs.tar.gz /libs.tar.gz

RUN tar -xvf /libs.tar.gz -C / && rm /libs.tar.gz && ldconfig

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

COPY --from=js-stage ${FUNCTION_DIR}/dist/*.html ${FUNCTION_DIR}/custom_admin/templates/astro/
COPY --from=js-stage ${FUNCTION_DIR}/dist/_astro ${FUNCTION_DIR}/custom_admin/static/_astro/

RUN USERS_SERVICE=empty \
    ASSOCIATION_BACKEND_SERVICE=empty \
    SERVICE_TO_SERVICE_SECRET=empty \
    GATEWAY_SERVICE=empty \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    PASTAPORTO_SECRET=demo \
    ${FUNCTION_DIR}/.venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
