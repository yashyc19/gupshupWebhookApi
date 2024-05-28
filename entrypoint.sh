#!/bin/sh

if [ -n "$GUNICORN_CMD_ARGS" ]; then
    exec gunicorn "$@"
else
    exec python app.py
fi