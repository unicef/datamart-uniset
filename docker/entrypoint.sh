#!/bin/bash


echo "Command: $@"

mkdir -p /var/uniset/{log,run}

/etc/init.d/redis-server stop
/etc/init.d/supervisor stop

if [[ "$*" == "uniset" ]];then

    set -ex
    db-isready --timeout 60

    echo "Initialize the database"
    SUPERSET_UPDATE_PERMS=1 uniset db upgrade

    echo "Create default roles and permissions"
    SUPERSET_UPDATE_PERMS=1 uniset init

    gunicorn    -w $WORKERS \
                --timeout 60 \
                -b  0.0.0.0:8088 \
                --limit-request-line 0 \
                --limit-request-field_size 0 \
                uniset.app:app
elif [[ "$*" == "celery" ]];then
    celery worker --app=superset.sql_lab:celery_app --pool=gevent -Ofair
elif [[ "$*" == "stack" ]];then
    exec circusd /etc/circus.conf
elif [[ "$*" == "dev" ]];then
    uniset runserver -d
else
    exec "$@"
fi
