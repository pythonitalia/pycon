ARG FUNCTION_DIR="/home/app/"

FROM python:3.11-slim as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apt-get update -y && apt-get install -y \
    gcc libpq-dev git \
    # Pillow
    libtiff5-dev libjpeg62 libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev libldap2-dev libldap-2.5-0 \
    ffmpeg libsm6 libxext6 libglib2.0-0

ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install pdm==2.10.4

RUN tar -czvf /libs.tar.gz /usr/lib/x86_64-linux-gnu/libpq* \
    /usr/lib/x86_64-linux-gnu/libpq* \
    /usr/lib/x86_64-linux-gnu/libldap_r* \
    /usr/lib/x86_64-linux-gnu/libldap* \
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
    /usr/lib/x86_64-linux-gnu/libtiff* \
    /usr/lib/x86_64-linux-gnu/libGL* \
    /usr/lib/x86_64-linux-gnu/libgthread* \
    /usr/lib/x86_64-linux-gnu/libglib-* \
    /usr/lib/x86_64-linux-gnu/libX11* \
    /usr/lib/x86_64-linux-gnu/libxcb* \
    /usr/lib/x86_64-linux-gnu/libXau* \
    /usr/lib/x86_64-linux-gnu/libXdmcp* \
    /usr/lib/x86_64-linux-gnu/libXext* \
    /usr/lib/x86_64-linux-gnu/libbsd*

COPY pyproject.toml pdm.lock ${FUNCTION_DIR}

RUN pdm install --prod --group lambda

# Create GraphQL schema

FROM python:3.11-slim as schema-stage

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv
COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /libs.tar.gz /libs.tar.gz

RUN tar -xvf /libs.tar.gz -C / && rm /libs.tar.gz && ldconfig

COPY . ${FUNCTION_DIR}

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    STRIPE_SECRET_API_KEY=demo \
    STRIPE_SUBSCRIPTION_PRICE_ID=demo \
    STRIPE_WEBHOOK_SIGNATURE_SECRET=demo \
    CELERY_BROKER_URL=demo \
    CELERY_RESULT_BACKEND=demo \
    HASHID_DEFAULT_SECRET_SALT=demo \
    ${FUNCTION_DIR}/.venv/bin/python manage.py graphql_schema

# Build custom admin components

FROM node:18.17.1 as js-stage

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

RUN npm install -g pnpm

COPY custom_admin/package.json custom_admin/pnpm-lock.yaml ./

RUN pnpm install

COPY custom_admin/ .

COPY --from=schema-stage ${FUNCTION_DIR}/schema.graphql schema.graphql

RUN ADMIN_GRAPHQL_URL=schema.graphql pnpm codegen
RUN pnpm build

# Final stage

FROM python:3.11-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=js-stage ${FUNCTION_DIR}/dist/*.html ${FUNCTION_DIR}/custom_admin/templates/astro/
COPY --from=js-stage ${FUNCTION_DIR}/dist/_astro ${FUNCTION_DIR}/custom_admin/static/_astro/

COPY --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv
COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /libs.tar.gz /libs.tar.gz

RUN tar -xvf /libs.tar.gz -C / && rm /libs.tar.gz && ldconfig

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    STRIPE_SECRET_API_KEY=demo \
    STRIPE_SUBSCRIPTION_PRICE_ID=demo \
    STRIPE_WEBHOOK_SIGNATURE_SECRET=demo \
    CELERY_BROKER_URL=demo \
    CELERY_RESULT_BACKEND=demo \
    HASHID_DEFAULT_SECRET_SALT=demo \
    ${FUNCTION_DIR}/.venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
