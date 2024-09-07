# ARG PRETIX_BASE_TAG
# FROM pyconit-local-pretix-base:${PRETIX_BASE_TAG}
FROM --platform=arm64 pretix/standalone:2024.7.0

COPY ./entrypoint.sh /entrypoint.sh
COPY ./settings.py /pretix/src/production_settings.py

USER root
RUN chown -R pretixuser:pretixuser /pretix
USER pretixuser

RUN pip install pretix-plugin-extended-api==0.1.12 pretix-plugin-attendance-certificate==0.1.11 pretix-fattura-elettronica==0.2.15

RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
RUN cd /pretix/src && DATABASE_HOST=demo make compress

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "all" ]
