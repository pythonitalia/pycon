# check=skip=SecretsUsedInArgOrEnv
ARG FUNCTION_DIR="/home/app"

FROM python:3.11-slim AS base

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

RUN apt-get update -y && apt-get install -y \
    # weasyprint
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
    # postgres - psycopg & also psql cli
    postgresql-client libpq-dev

FROM base AS build-stage

ARG FUNCTION_DIR

RUN apt-get update -y && apt-get install -y \
    gcc git

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN pip install uv==0.5.5

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY . ./

RUN .venv/bin/python manage.py graphql_schema

# Build custom admin components

FROM node:23 AS js-stage

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

RUN npm install -g pnpm

COPY custom_admin/package.json custom_admin/pnpm-lock.yaml ./

RUN pnpm install

COPY --from=build-stage ${FUNCTION_DIR}/schema.graphql schema.graphql

COPY custom_admin/ .

RUN ADMIN_GRAPHQL_URL=schema.graphql pnpm codegen && pnpm build

# Runtime stage

FROM base AS runtime-stage

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

ENV LIBRARY_PATH=/lib:/usr/lib LD_LIBRARY_PATH=/lib:/usr/lib

RUN apt-get update -y && apt-get install -y curl

RUN groupadd -r app && useradd -r -g app app && mkdir -p ${FUNCTION_DIR} && chown -R app:app ${FUNCTION_DIR}

COPY --chown=app:app --from=js-stage ${FUNCTION_DIR}/dist/*.html ${FUNCTION_DIR}/custom_admin/templates/astro/
COPY --chown=app:app --from=js-stage ${FUNCTION_DIR}/dist/_astro ${FUNCTION_DIR}/custom_admin/static/_astro/
COPY --chown=app:app --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv

COPY --chown=app:app . ${FUNCTION_DIR}

USER app

RUN mkdir -p assets && .venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/gunicorn"]
CMD [ "pycon.wsgi" ]
