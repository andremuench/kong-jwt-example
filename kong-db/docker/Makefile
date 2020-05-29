IMAGE = postgres:12
CONTAINER = kong-database
NETWORK = kong-net

THIS_FILE := $(realpath $(lastword $(MAKEFILE_LIST)))
THIS_FILE_DIR := $(shell dirname $(THIS_FILE))


build:
	DOCKER_BUILDKIT=1 docker build -f $(THIS_FILE_DIR)/Dockerfile \
		-t $(IMAGE) \
		$(THIS_FILE_DIR)/../source

run:
	docker run -d \
		--name ${CONTAINER} \
		--net ${NETWORK} \
		-e POSTGRES_USER=kong \
		-e POSTGRES_DB=kong \
		${IMAGE}

stop:
	docker stop ${CONTAINER}

rm: stop
	docker rm ${CONTAINER}

help:
	$(info Use `make check` to check if environment is ready)
	$(info Use `make build` to build image)
	$(info Use `make run` to start container)
	$(info Use `make stop` to stop container)
	$(info Use `make rm` to remove container)
