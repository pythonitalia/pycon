#!/bin/sh -l

# copy our folder to a temporary folder to prevent permission issues
cp -R infrastructure/eb /tmp/eb
cd /tmp/eb/$INPUT_ENV

eb "$@"
