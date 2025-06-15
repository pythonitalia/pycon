FROM ghcr.io/pythonitalia/pycon/base-pretix:v2025.5.0

COPY ./settings.py /pretix/src/production_settings.py

RUN pip install boto3==1.38.36 \
    django-storages==1.14.6 \
    pretix-plugin-extended-api==0.1.14 \
    pretix-plugin-attendance-certificate==0.1.11 \
    pretix-fattura-elettronica==0.2.16 \
    pretix-plugin-advanced-stats==1.0.0

RUN cd /pretix/src && DATABASE_HOST=demo make staticfiles
RUN cd /pretix/src && DATABASE_HOST=demo make compress

ENTRYPOINT ["pretix"]
CMD [ "all" ]
