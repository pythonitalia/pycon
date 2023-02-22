ARG FUNCTION_DIR="/home/app/"

FROM python:3.9-slim as build-stage

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

RUN apt-get update -y && apt-get install -y gcc libpq-dev

ENV LIBRARY_PATH=/lib:/usr/lib

COPY poetry.lock ${FUNCTION_DIR}
COPY pyproject.toml ${FUNCTION_DIR}

RUN pip3 install poetry==1.1.13

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev -E lambda

FROM python:3.9-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-stage ${FUNCTION_DIR}/.venv ${FUNCTION_DIR}/.venv

RUN mkdir -p ${FUNCTION_DIR}/assets

COPY . ${FUNCTION_DIR}

ENTRYPOINT ["/home/app/.venv/bin/python", "-m", "awslambdaric"]
CMD [ "main.handler" ]
