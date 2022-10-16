FROM pretix/standalone:4.13.1

COPY ./entrypoint.sh /entrypoint.sh
COPY ./settings.py /pretix/src/production_settings.py

USER root
RUN chown -R pretixuser:pretixuser /pretix
USER pretixuser

RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
RUN cd /pretix/src && DATABASE_HOST=demo make compress

RUN pip install pretix-plugin-extended-api==0.1.9

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "all" ]
