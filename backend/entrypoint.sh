#!/bin/sh

echo "Fixing permissions"
chown -R app:app /tmp

exec su - app -c "exec $*"