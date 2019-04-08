FROM python:3.6.8-alpine3.8

ARG BUILD_DATE
ARG PIPENV_ARGS
ARG VERSION
ARG DEVELOP

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

#RUN apk add --no-cache --virtual .fetch-deps \
#        curl \
#        ca-certificates \
#        openssl \
#        tar
#
RUN apk add --no-cache --virtual .build-deps \
        autoconf \
        automake \
        pkgconf \
        g++ \
        json-c-dev \
        libtool \
        libxml2-dev \
        make \
        perl
#
#RUN apk add --no-cache --virtual .build-deps-edge \
#        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
#        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
#        proj4-dev \
#        protobuf-c-dev
#
#RUN apk add --no-cache --virtual .postgis-rundeps \
#        json-c
#
#RUN apk add --no-cache --virtual .postgis-rundeps-edge \
#        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
#        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
#        binutils \
#        geos \
#        geos-dev \
#        gdal-dev \
#        gdal \
#        proj4 \
#        protobuf-c
#
RUN apk add --no-cache --virtual .datamart-build-deps \
        freetype-dev \
        cyrus-sasl-dev \
        fontconfig-dev \
        freetype-dev \
        jpeg-dev \
        lcms2-dev \
        libffi-dev \
        libressl-dev \
        linux-headers \
        musl-dev \
        openjpeg-dev \
        postgresql-dev \
        python3-dev \
        tcl-dev \
        tiff-dev \
        tk-dev \
        zlib-dev

RUN apk add --no-cache --virtual .datamart-run-deps \
        postgresql-libs

RUN apk add --no-cache --virtual .system-run-deps \
        bash

RUN mkdir -p /code
ADD . /code
WORKDIR /code

RUN set -ex \
    ls -al /code \
    && cat src/uniset/__init__.py | grep VERSION \
    && pip install -r freeze.txt \
    && pip install -e .

RUN apk del .fetch-deps .build-deps .build-deps-edge .datamart-build-deps

ADD docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["uniset"]
