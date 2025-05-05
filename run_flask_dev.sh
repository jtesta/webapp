#!/bin/bash


echo "Running Flask development service on http://0.0.0.0:8000/"

FLASK_CONFIG_FILE=${PWD}/webapp.cfg flask --app webapp run --host 127.0.0.1 -p 8000 --debug
