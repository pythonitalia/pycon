#!/bin/sh
set -e

chown -R app:app /tmp

exec su -p app -c "exec $*"