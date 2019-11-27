# version 1.1

FROM pretix/standalone:stable

COPY ./entrypoint.sh /entrypoint.sh
COPY ./pretix.template.cfg /pretix/pretix.template.cfg

ENV PRETIX_CONFIG_FILE=/pretix/pretix.cfg

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "all" ]
