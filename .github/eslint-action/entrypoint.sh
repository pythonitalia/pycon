#!/bin/sh -l

cd pycon-frontend

yarn install

NODE_PATH=node_modules node /action/run.js
