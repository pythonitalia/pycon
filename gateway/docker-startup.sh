#!/bin/bash
if [ ! -f ".variant" ]; then
    echo ".variant does not exist. Creating it."
    uuid=$(cat /proc/sys/kernel/random/uuid)
    echo $uuid
    variant=${uuid//-/}
    echo $variant > .variant
else
    echo ".variant exists. Re-using it."
    variant=$(cat .variant)
fi

export APOLLO_GRAPH_VARIANT=$variant
touch .ready
yarn dev
