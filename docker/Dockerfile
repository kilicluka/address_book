FROM python:3.10.0-alpine3.14 AS base

ENV APP_GROUP server
ENV APP_USER server
ENV PROJECT_DIR /srv

RUN set -ex \
    && apk update \
    && apk add  \
      postgresql-dev \
      sudo \
    && apk add --virtual .build-deps \
      gcc \
      musl-dev

RUN set -ex \
    && addgroup \
      -S ${APP_GROUP} \
      -g 1000 \
    && adduser \
      -S ${APP_USER} \
      -G ${APP_GROUP} \
      -h ${PROJECT_DIR} \
      -u 1000 \
    && echo "${APP_GROUP} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${APP_GROUP}

WORKDIR ${PROJECT_DIR}/src

COPY requirements/common.txt /srv/requirements/

RUN set -ex \
    && pip3 install -r /srv/requirements/common.txt \
    && apk del .build-deps

COPY src/ ${PROJECT_DIR}/src/


FROM base as production

RUN set -ex && rm -rf /srv/requirements

RUN set -ex && chown -R ${APP_USER}:${APP_USER} ${PROJECT_DIR}

USER ${APP_USER}


FROM base as development

COPY requirements/dev.txt /srv/requirements/

RUN set -ex \
    && pip3 install -r /srv/requirements/dev.txt \
    && rm -rf /srv/requirements

RUN set -ex && chown -R ${APP_USER}:${APP_USER} ${PROJECT_DIR}

USER ${APP_USER}
