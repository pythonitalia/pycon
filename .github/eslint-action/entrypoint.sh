#!/bin/sh -l

cd frontend

yarn install

NODE_PATH=node_modules node /action/run.js