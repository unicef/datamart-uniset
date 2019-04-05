CMD?=
TARGET?=0.1.0a0
PIPENV_PYPI_MIRROR?=https://pypi.org/simple/
DOCKER_IMAGE?=unicef/uniset
DOCKERFILE?=docker/Dockerfile
BUILD_OPTIONS?=--squash --compress --rm
DEVELOP?="0"
WORKERS?=1

help:
	@echo 'Options:                                                       '
	@echo '   options can be passed via environment variables             '
	@echo '   TARGET:   package version and tag                           '
	@echo '   DEVELOP:  1=Use local code - 0=feth release from github     '
	@echo 'Usage:                                                         '
	@echo '   make clean            removes images and containers         '
	@echo '   make build            build container                       '
	@echo '   make test             test container                        '
	@echo '   make run              run container (only app)              '
	@echo '   make stack            run container (stack celery/redis)    '
	@echo '   make shell                                                  '
	@echo '   make push             push image to docker hub              '
	@echo '                                                               '
	@echo 'Examples'
	@echo '`DEVELOP=1 make build`'
	@echo '    Build unicef/uniset:dev using local code'
	@echo '`TARGET1.3a DEVELOP=1 make build`'
	@echo '    Build unicef/uniset:1.3a using local code'
	@echo '`TARGET1.3 make build`'
	@echo '    Build unicef/uniset:1.3 fetching uniset-1.3.tar.gz from GitHub'


clean:
	docker rmi --force ${DOCKER_IMAGE}:${TARGET}

dev:
	DEVELOP=1 $(MAKE) build

build:
	cd .. && docker build ${BUILD_OPTIONS} \
			--build-arg PIPENV_ARGS=--pypi-mirror=${PIPENV_PYPI_MIRROR} \
			--build-arg DEVELOP=${DEVELOP} \
			--build-arg GITHUB_CREDENTIALS=${GITHUB_TOKEN} \
			--build-arg VERSION=${TARGET} \
			--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
			-t ${DOCKER_IMAGE}:${TARGET} \
			-f ${DOCKERFILE} .
	@docker images | grep ${DOCKER_IMAGE}
#	@docker inspect --format "{{ index .Config.Labels}}" ${DOCKER_IMAGE}:${TARGET}
#	@docker history ${DOCKER_IMAGE}:${TARGET}

.run:
	cd .. && docker run \
			-p 5000:5000 \
			-p 8088:8088 \
			-p 5555:5555 \
			--rm \
			-e SECRET_KEY=${SECRET_KEY} \
			-e MAPBOX_API_KEY=${MAPBOX_API_KEY} \
			-e DATABASE_URL=${DATABASE_URL} \
			-e ADMIN_USERNAME=${ADMIN_USERNAME} \
			-e ADMIN_PASSWORD=${ADMIN_PASSWORD} \
			-e ADMIN_EMAIL=${ADMIN_EMAIL} \
			-e AZURE_CLIENT_ID=${AZURE_CLIENT_ID} \
			-e AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET} \
			-e CACHE_REDIS_URL=${CACHE_REDIS_URL} \
			-e CELERY_BROKER_URL=${CELERY_BROKER_URL} \
			-e CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND} \
			-e WORKERS=${WORKERS} \
			--name uniset \
			-it ${DOCKER_IMAGE}:${TARGET} \
			${CMD}

run:
	$(MAKE) .run

test:
	CMD='uniset check' $(MAKE) .run

stack:
	CMD='stack' $(MAKE) run

shell:
	CMD='/bin/bash' $(MAKE) run

push:
	docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
	docker tag ${DOCKER_IMAGE}:${TARGET} ${DOCKER_IMAGE}:latest
	docker push ${DOCKER_IMAGE}:${TARGET}
	docker push ${DOCKER_IMAGE}:latest


.PHONY: run
