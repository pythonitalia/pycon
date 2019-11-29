#!/bin/sh -l

cp /pretix/pretix.template.cfg /pretix/pretix.cfg

awk '{
    gsub("{{database_name}}", "'$DATABASE_NAME'" , $0);
    gsub("{{database_username}}", "'$DATABASE_USERNAME'" , $0);
    gsub("{{database_password}}", "'$DATABASE_PASSWORD'" , $0);
    gsub("{{database_host}}", "'$DATABASE_HOST'" , $0);

    gsub("{{mail_user}}", "'$MAIL_USER'" , $0);
    gsub("{{mail_password}}", "'$MAIL_PASSWORD'" , $0);
    gsub("{{sentry_dsn}}", "'$SENTRY_DSN'" , $0);

    gsub("{{url}}", "'$URL'" , $0);
    print $0 > "/pretix/pretix.cfg";
}' /pretix/pretix.template.cfg

awk '{
    gsub("{{database_name}}", "'$DATABASE_NAME'" , $0);
    gsub("{{database_username}}", "'$DATABASE_USERNAME'" , $0);
    gsub("{{database_password}}", "'$DATABASE_PASSWORD'" , $0);
    gsub("{{database_host}}", "'$DATABASE_HOST'" , $0);

    gsub("{{mail_user}}", "'$MAIL_USER'" , $0);
    gsub("{{mail_password}}", "'$MAIL_PASSWORD'" , $0);
    gsub("{{sentry_dsn}}", "'$SENTRY_DSN'" , $0);

    gsub("{{url}}", "'$URL'" , $0);
    print $0 > "/pretix/src/production_settings.py";
}' /pretix/src/production_settings.py

pretix "$@"
