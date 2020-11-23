#!/bin/bash
if [ ! -e secret.yaml ]; then
    gsutil cp gs://flask_template_secrets/secret.yaml secret.yaml
fi
if [ ! -e secret.json ]; then
    gsutil cp gs://flask_template_secrets/secret.json secret.json
fi

export FLASK_DEBUG=TRUE
export FLASK_APP=main.py
export GCS_ROOT_PATH='gs://flask-template/uploads'
flask run 
