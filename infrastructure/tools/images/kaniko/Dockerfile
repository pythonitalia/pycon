FROM gcr.io/kaniko-project/executor:debug AS kaniko

FROM ghcr.io/actions/actions-runner:2.321.0

COPY --from=kaniko /kaniko/ /kaniko/

ENV SSL_CERT_DIR /kaniko/ssl/certs
ENV PATH $PATH:/usr/local/bin:/kaniko
ENV DOCKER_CONFIG /kaniko/.docker/

ENV RUNNER_ALLOW_RUNASROOT 1
USER root
RUN groupadd messagebus || true
