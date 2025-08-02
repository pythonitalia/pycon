#!/bin/sh

echo "Fixing permissions"
chown -R app:app /tmp

su - app -c "$@"