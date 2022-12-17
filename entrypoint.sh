#!/usr/bin/env bash

# TODO: preconvert images options
# TODO: preconvery models options

# update the DB
flask db upgrade

# RUNNNNNNNNNNNNN
gunicorn -b :8000 -w 4 wsgi:app
