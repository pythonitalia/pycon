#!/bin/bash

python3 ws.py &

/usr/local/openresty/bin/openresty -g 'daemon off;'

wait -n

exit $?
