FROM pstauffer/curl:latest as builder
ARG VERSION
ARG GITHUB_TOKEN
ARG DEVELOP

LABEL MAINTANER=UNICEF
LABEL Versio=$VERSION
LABEL Date=$BUILD_DATE

RUN mkdir /code
WORKDIR /code
ADD . /code

RUN if [ "$DEVELOP" = "1" ]; then \
    echo "$VERSION-develop"; \
    else \
    echo "Download package: https://github.com/unicef/uniset/archive/${VERSION}.tar.gz" \
    && curl -u ${GITHUB_TOKEN}: -L "https://github.com/unicef/uniset/archive/${VERSION}.tar.gz" | tar -xzf - --strip-components=1; \
    fi

FROM python:3.6.4

ARG PIPENV_ARGS
ARG TAG

ENV ADMIN_USERNAME ""
ENV ADMIN_PASSWORD ""
ENV ADMIN_EMAIL ""

ENV WORKERS 2

RUN set -ex && apt-get -q update && apt-get install -y \
    libsasl2-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8
RUN set -ex \
    && pip install pip pipenv --upgrade \
    && mkdir /app

WORKDIR /app

ENV PYTHONPATH=/etc/superset

COPY VERSION /
COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/

COPY ./entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ./entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY ./datamart.tpl.yaml /etc/datamart.tpl.yaml

RUN set -ex && pipenv install --deploy --system --ignore-pipfile $PIPENV_ARGS

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["uniset"]
