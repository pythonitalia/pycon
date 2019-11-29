# version 1.1

FROM pretix/standalone:stable

COPY ./entrypoint.sh /entrypoint.sh
COPY ./pretix.template.cfg /pretix/pretix.template.cfg
COPY ./settings.py /pretix/src/production_settings.py

USER root
RUN chown -R pretixuser:pretixuser /pretix
USER pretixuser

RUN touch /pretix/pretix.cfg
RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
RUN cd /pretix/src && DATABASE_HOST=demo make compress

ENV PRETIX_CONFIG_FILE=/pretix/pretix.cfg

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "all" ]
