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
    cargo \
    automake

RUN apk add --no-cache --virtual .build-deps postgresql-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip3 install awslambdaric

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM python:3.9-alpine

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY --from=build-stage /usr/local/lib/*.so* /usr/local/lib/
COPY --from=build-stage /usr/lib/libpq.so.5 \
    /usr/lib/libpq.so.5 \
    /usr/lib/libldap_r-2.4.so.2 \
    /usr/lib/liblber-2.4.so.2 \
    /usr/lib/libsasl2.so.3 \
    /usr/lib/libxslt.so.1 \
    /usr/lib/libexslt.so.0 \
    /usr/lib/libxml2.so.2 \
    /usr/lib/libgcrypt.so.20 \
    /usr/lib/libgpg-error.so.0 \
    /usr/lib/libstdc++.so.6 \
    /usr/lib/libgcc_s.so.1 \
    /usr/lib/

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD [ "main.handler" ]
