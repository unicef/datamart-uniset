#!/bin/bash

superset init
initialized=$?

set -ex

if [ $initialized != 0 ];then

    fabmanager create-admin --app superset \
                            --username "$ADMIN_USERNAME" \
                            --password "$ADMIN_PASSWORD" \
                            --firstname "" \
                            --lastname "" \
                            --email "$ADMIN_EMAIL"

    cat /etc/datamart.tpl.yaml | sed "s|DATAMART_DATABASE_URL|$DATAMART_DATABASE_URL|" > /etc/datamart.yaml
    superset import_datasources -p /etc/datamart.yaml
    # Initialize the database
    superset db upgrade

    # Create default roles and permissions
    superset init

fi


echo "Command: $1"

if [ "$1" == "uniset" ];then
    gunicorn -w 2 --timeout 60 -b  0.0.0.0:8088 --limit-request-line 0 --limit-request-field_size 0 uniset.app:app
elif [ "$1" == "dev" ];then
    uniset runserver -d
else
    exec "$@"
fi
#
#
#if [ "$#" -ne 0 ]; then
#    exec "$@"
#elif [ "$SUPERSET_ENV" = "local" ]; then
#    superset runserver -d
#elif [ "$SUPERSET_ENV" = "production" ]; then
#    superset runserver -a 0.0.0.0 -w $((2 * $(getconf _NPROCESSORS_ONLN) + 1))
#else
#    superset --help
#fi
