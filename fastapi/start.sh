#! /bin/sh

gunicorn --preload -c gunicorn.conf.py main:app