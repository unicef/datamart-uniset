UNISET
======

[![CircleCI](https://circleci.com/gh/unicef/uniset.svg?style=svg)](https://circleci.com/gh/unicef/uniset)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e302b4b24d7b473a8b34a9a7d27d2a92)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=unicef/uniset&amp;utm_campaign=Badge_Grade)
[![](https://images.microbadger.com/badges/version/unicef/uniset.svg)](https://microbadger.com/images/unicef/uniset)

UNICEF custom distribution of [superset](https://superset.incubator.apache.org/).

This repo contains a customized distribution of [superset](https://superset.incubator.apache.org/), business intelligence analisys tool.

Extras
------

- ability to load users from UNICEF AD and grant them specif roles, without force them to login


##### TODO:

- Login using Organization's Active Directory
- Send email to user to with account/granted privileges informations


Quickstart
----------

    createdb uniset
    uniset db upgrade
    fabmanager create-admin \
            --app superset \
            --username "admin" \
            --password <PASSWORD> \
            --firstname "" \
            --lastname "" \
            --email <EMAIL>
    uniset runserver -d
