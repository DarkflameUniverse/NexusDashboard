#!/usr/bin/env bash

# TODO: preconvert images options
# TODO: preconvery models options

# update the DB
flask db upgrade

# RUNNNNNNNNNNNNN
gunicorn --reload ${RELOAD_EXTRA_FILE:+--reload-extra-file ${RELOAD_EXTRA_FILE}} -b :8000 -w 4 wsgi:app
