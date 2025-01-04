FROM gcr.io/kaniko-project/executor:debug AS kaniko

FROM ghcr.io/actions/actions-runner:2.321.0

USER runner

COPY --chown=runner:docker --from=kaniko /kaniko/ /kaniko/

ENV SSL_CERT_DIR /kaniko/ssl/certs
ENV PATH $PATH:/usr/local/bin:/kaniko
ENV DOCKER_CONFIG /kaniko/.docker/
