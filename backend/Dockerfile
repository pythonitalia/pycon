ARG FUNCTION_DIR="/home/app/"

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
    /usr/lib/x86_64-linux-gnu/libjbig* \
    /usr/lib/x86_64-linux-gnu/liblcms2* \
    /usr/lib/x86_64-linux-gnu/libwebp* \
    /usr/lib/x86_64-linux-gnu/libtiff*

RUN pip3 install poetry==1.1.13

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

RUN USERS_SERVICE=empty \
    ASSOCIATION_BACKEND_SERVICE=empty \
    SERVICE_TO_SERVICE_SECRET=empty \
    CFP_SLACK_INCOMING_WEBHOOK_URL=example \
    SUBMISSION_COMMENT_SLACK_INCOMING_WEBHOOK_URL=example \
    AWS_MEDIA_BUCKET=example \
    AWS_REGION_NAME=eu-central-1 \
    SECRET_KEY=DEMO \
    PASTAPORTO_SECRET=demo \
    ${FUNCTION_DIR}/.venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/home/app/.venv/bin/python", "-m", "awslambdaric"]
CMD [ "wsgi_handler.handler" ]
