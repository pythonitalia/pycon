ARG PRETIX_IMAGE
FROM ${PRETIX_IMAGE}

COPY ./settings.py /pretix/src/production_settings.py

RUN pip install pretix-plugin-extended-api==0.1.12 pretix-plugin-attendance-certificate==0.1.11 pretix-fattura-elettronica==0.2.15

# RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
# RUN cd /pretix/src && DATABASE_HOST=demo make compress

ENTRYPOINT ["pretix"]
CMD [ "all" ]
