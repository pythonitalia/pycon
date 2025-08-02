#!/bin/sh

echo "Fixing permissions"
chown -R app:app /tmp

exec sudo -u app "$@"