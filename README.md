UNISET
======

[![CircleCI](https://circleci.com/gh/unicef/uniset.svg?style=svg)](https://circleci.com/gh/unicef/uniset)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e302b4b24d7b473a8b34a9a7d27d2a92)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=unicef/uniset&amp;utm_campaign=Badge_Grade)
[![](https://images.microbadger.com/badges/version/unicef/uniset.svg)](https://microbadger.com/images/unicef/uniset)

UNICEF custom distribution of [superset].

This repo contains a customized distribution of [superset], business intelligence analisys tool.

Extras
------

- ability to load users from UNICEF AD and grant them specif roles, without force them to login
- Login using Organization's Active Directory
- Auto creation of admins if listed in ADMINS config list 


##### TODO:

- Send email to user to with account/granted privileges informations
- Merging existing records with oauth accounts 


Warning Notes
-------------

Stable [superset] version (0.28.1 at time of writing) contaions a bug that prevent
to override default SecurityManager

To enable UNICEF Azure integration, some monkeypatches need to be applied during 
Flask initialization (see `uniset.monkeypatch`)

Another bug in [flask_appbuilder], does not allow the use of `ADDON_MANAGERS`
extension point with python 3.6. For this reason it is not used in uniset,
extensions and custom views are configured in `uniset.app`, for this reason `uniset.app:app`
must be used with gunicorn instead of the classical `superset`

Most of those bugs have been resolved, and will be released in the next versions of relative packages,
when them will be officially released, related monkeypatches will be removed.

[superset]:https://superset.incubator.apache.org/
[flask_appbuilder]:https://secure.travis-ci.org/bitcaster-io/bitcaster.png?branch=develop
