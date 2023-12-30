FROM pretix/standalone:4.18.2

COPY ./entrypoint.sh /entrypoint.sh
COPY ./settings.py /pretix/src/production_settings.py

USER root
RUN chown -R pretixuser:pretixuser /pretix
USER pretixuser

RUN pip install pretix-plugin-extended-api==0.1.10 pretix-plugin-attendance-certificate==0.1.7 pretix-fattura-elettronica==0.2.2

RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
RUN cd /pretix/src && DATABASE_HOST=demo make compress

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "all" ]
