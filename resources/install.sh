#!/bin/sh

dockerCompose=$(which docker-compose)

ver=$(python -V 2>&1 | sed "s/.* \([0-9]\).\([0-9]\).*/\1\2/")
if [ "$ver" -lt "38" ]; then
    echo "This script requires python 3.8 or greater"
    exit 1
fi

# copy default env vars
if [ ! -f .env ]; then
    cp .env.dist .env
fi
export $(grep -v '^#' .env | xargs -d '\n')

# $dockerCompose up -d

if [ ! -d "venv" ];then
  python -m venv venv
  . venv/bin/activate
fi

pip install -r requirements.txt

# ./manage.py migrate

# show result
if [ $? -eq 0 ]; then
    echo ""
    echo "Successfully installed!"
    echo "Please run ./manage.py createsuperuser"
    echo "to install admin user if needed"
    echo ""
else
    echo ""
    echo "Something went wrong. Fix the errors and try again."
    echo ""
fi
