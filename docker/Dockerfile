FROM pstauffer/curl:latest as builder
ARG DEVELOP
ARG GITHUB_CREDENTIALS
ARG VERSION

RUN mkdir /code
WORKDIR /code
ADD . /code

RUN if [ "${DEVELOP}" = "1" ]; then \
    echo "${VERSION}-develop"; \
    else \
    echo "Download package: https://github.com/unicef/uniset/archive/${VERSION}.tar.gz" \
    && curl ${GITHUB_CREDENTIALS}: -L "https://github.com/unicef/uniset/archive/${VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
    fi

FROM python:3.6.8
ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION

LABEL MAINTANER=UNICEF
LABEL Versio=$VERSION
LABEL Date=$BUILD_DATE

ENV PIPENV_ARGS ${PIPENV_ARGS}
ENV LANG C.UTF-8

ENV ADMIN_USERNAME ""
ENV ADMIN_PASSWORD ""
ENV ADMIN_EMAIL ""
ENV WORKERS 10
ENV AZURE_CLIENT_ID ""
ENV AZURE_CLIENT_SECRET ""
ENV SUPERSET_UPDATE_PERMS 0
ENV CACHE_REDIS_URL "redis://127.0.0.1:6379/9"

ENV START_UNISET "true"
ENV START_REDIS "true"
ENV START_CELERY "true"

ENV SUPERVISOR_USER "admin"
ENV SUPERVISOR_PWD "admin"


ADD docker/redis.conf /etc/redis.conf
ADD docker/db-isready.py /usr/local/bin/db-isready
ADD docker/wait-for-it.sh /usr/local/bin/wait-for-it
ADD docker/circus.conf /etc/circus.conf

RUN set -ex \
    && apt-get -q update \
    && apt-get install -y \
        libsasl2-dev \
        circus \
        redis-server \
        gcc \
    && chmod +x /usr/local/bin/wait-for-it \
    && chmod +x /usr/local/bin/db-isready \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pip

WORKDIR /code
COPY --from=builder /code /code
RUN set -ex \
    ls -al /code \
    && cat src/uniset/__init__.py | grep VERSION \
    && pip install -r freeze.txt \
    && pip install -e .

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["uniset"]
