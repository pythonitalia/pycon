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

COPY pyproject.toml pdm.lock ${FUNCTION_DIR}

RUN pdm install --prod --group lambda

FROM python:3.11-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv
RUN ls -al /home/app/.venv/lib/python3.11/site-packages/temporalio/bridge/
COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /usr/lib/*.so* /usr/lib/

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENV DJANGO_SETTINGS_MODULE=pycon.settings.prod

RUN DJANGO_SETTINGS_MODULE=pycon.settings.test \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    STRIPE_SECRET_API_KEY=demo \
    STRIPE_SUBSCRIPTION_PRICE_ID=demo \
    STRIPE_WEBHOOK_SIGNATURE_SECRET=demo \
    ${FUNCTION_DIR}/.venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
