FROM mini/base

ARG AWSEBCLI_VERSION=3.15.3

RUN apk-install \
    git \
    python3 \
  && pip3 install --no-cache-dir --upgrade \
    awsebcli==$AWSEBCLI_VERSION \
  && adduser -D aws

USER aws

VOLUME ["/data"]

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]