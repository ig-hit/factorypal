#!/bin/sh

export $(grep -v '^#' .env | xargs -d '\n')
python ./manage.py runserver ${BASE_PORT}
