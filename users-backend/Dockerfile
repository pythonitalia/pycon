ARG FUNCTION_DIR="/home/app/"

FROM python:3.9-slim as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

# RUN apt-get update -y && apt-get install -y build-base jpeg-dev zlib-dev libxml2-dev libxslt-dev postgresql-libs make cmake libtool \
#     autoconf \
#     libexecinfo-dev \
#     libcurl \
#     gcc \
#     musl-dev \
#     python3-dev \
#     libffi-dev \
#     openssl-dev \
#     cargo \
#     automake

# RUN apt-get install -y --no-cache --virtual .build-deps postgresql-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip3 install awslambdaric

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM python:3.9-slim

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
    /usr/lib/

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD [ "main.handler" ]
