#!/bin/bash
if [ ! -e secret.yaml ]; then
    gsutil cp gs://vape-survey-secrets/secret.yaml secret.yaml
fi
if [ ! -e secret.json ]; then
    gsutil cp gs://vape-survey-secrets/secret.json secret.json
fi

export FLASK_DEBUG=TRUE
export FLASK_APP=main.py
export GCS_ROOT_PATH='gs://vape-survey/uploads'
export GOOGLE_APPLICATION_CREDENTIALS="./secret.json"
flask run 
