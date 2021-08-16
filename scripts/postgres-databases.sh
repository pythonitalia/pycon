#!/bin/bash

set -e
set -u

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE pycon;
    GRANT ALL PRIVILEGES ON DATABASE pycon TO pythonitalia;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE users;
    GRANT ALL PRIVILEGES ON DATABASE users TO pythonitalia;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE association;
    GRANT ALL PRIVILEGES ON DATABASE association TO pythonitalia;
EOSQL
