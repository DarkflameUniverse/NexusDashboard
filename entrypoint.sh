#!/usr/bin/env bash

# unzip brickdb from client to the right places
unzip -n -q /app/luclient/res/brickdb.zip -d app/luclient/res/

# TODO: preconvert images options
# TODO: preconvery models options

# update the DB
flask db upgrade

# RUNNNNNNNNNNNNN
gunicorn -b :8000 -w 4 wsgi:app
