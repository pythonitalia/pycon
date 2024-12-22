ARG FUNCTION_DIR="/home/app"

FROM python:3.11-slim as base

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    STRIPE_SECRET_API_KEY=demo \
    STRIPE_SUBSCRIPTION_PRICE_ID=demo \
    STRIPE_WEBHOOK_SIGNATURE_SECRET=demo \
    CELERY_BROKER_URL=demo \
    CELERY_RESULT_BACKEND=demo \
    HASHID_DEFAULT_SECRET_SALT=demo

FROM base as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apt-get update -y && apt-get install -y \
    gcc libpq-dev git \
    # Pillow
    libtiff5-dev libjpeg62 libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev libldap2-dev libldap-2.5-0 \
    ffmpeg libsm6 libxext6 libglib2.0-0 libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0

ENV LIBRARY_PATH=/lib:/usr/lib LD_LIBRARY_PATH=/lib:/usr/lib

RUN pip install uv==0.5.5

RUN tar -czvf /libs.tar.gz \
        /usr/lib/aarch64-linux-gnu/libpq* \
        /usr/lib/aarch64-linux-gnu/libldap_r* \
        /usr/lib/aarch64-linux-gnu/libldap* \
        /usr/lib/aarch64-linux-gnu/liblber* \
        /usr/lib/aarch64-linux-gnu/libsasl* \
        /usr/lib/aarch64-linux-gnu/libxml2* \
        /usr/lib/aarch64-linux-gnu/libgcrypt* \
        /usr/lib/aarch64-linux-gnu/libstdc++* \
        /usr/lib/aarch64-linux-gnu/libjpeg* \
        /usr/lib/aarch64-linux-gnu/libopenjp2* \
        /usr/lib/aarch64-linux-gnu/libdeflate* \
        /usr/lib/aarch64-linux-gnu/libjbig* \
        /usr/lib/aarch64-linux-gnu/liblcms2* \
        /usr/lib/aarch64-linux-gnu/libwebp* \
        /usr/lib/aarch64-linux-gnu/libtiff* \
        /usr/lib/aarch64-linux-gnu/libGL* \
        /usr/lib/aarch64-linux-gnu/libgthread* \
        /usr/lib/aarch64-linux-gnu/libglib-* \
        /usr/lib/aarch64-linux-gnu/libX11* \
        /usr/lib/aarch64-linux-gnu/libxcb* \
        /usr/lib/aarch64-linux-gnu/libXau* \
        /usr/lib/aarch64-linux-gnu/libXdmcp* \
        /usr/lib/aarch64-linux-gnu/libXext* \
        /usr/lib/aarch64-linux-gnu/libbsd* \
        /usr/lib/aarch64-linux-gnu/libpango* \
        /usr/lib/aarch64-linux-gnu/libharf* \
        /usr/lib/aarch64-linux-gnu/libharfbuzz* \
        /usr/lib/aarch64-linux-gnu/libgobject*;

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY . ./

RUN .venv/bin/python manage.py graphql_schema

# Build custom admin components

FROM node:23 as js-stage

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

RUN npm install -g pnpm

COPY custom_admin/package.json custom_admin/pnpm-lock.yaml ./

RUN pnpm install

COPY --from=build-stage ${FUNCTION_DIR}/schema.graphql schema.graphql

COPY custom_admin/ .

RUN ADMIN_GRAPHQL_URL=schema.graphql pnpm codegen
RUN pnpm build

# Runtime stage

FROM base

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

ENV LIBRARY_PATH=/lib:/usr/lib LD_LIBRARY_PATH=/lib:/usr/lib

RUN apt-get update -y && apt-get install -y curl

RUN groupadd -r app && useradd -r -g app app && mkdir -p ${FUNCTION_DIR} && chown -R app:app ${FUNCTION_DIR}

COPY --chown=app:app --from=js-stage ${FUNCTION_DIR}/dist/*.html ${FUNCTION_DIR}/custom_admin/templates/astro/
COPY --chown=app:app --from=js-stage ${FUNCTION_DIR}/dist/_astro ${FUNCTION_DIR}/custom_admin/static/_astro/
COPY --chown=app:app --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv

COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /lib/aarch64-linux-gnu/*.so* /lib/aarch64-linux-gnu/
COPY --from=build-stage /libs.tar.gz /libs.tar.gz

RUN tar -xvf /libs.tar.gz -C / && rm /libs.tar.gz && ldconfig

COPY --chown=app:app . ${FUNCTION_DIR}

USER app

RUN mkdir -p assets

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN .venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/gunicorn"]
CMD [ "pycon.wsgi" ]
