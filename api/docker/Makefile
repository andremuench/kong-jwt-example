IMAGE = flask-api
CONTAINER = flask-api
NETWORK = kong-net

THIS_FILE := $(realpath $(lastword $(MAKEFILE_LIST)))
THIS_FILE_DIR := $(shell dirname $(THIS_FILE))

build:
	DOCKER_BUILDKIT=1 docker build \
		-t $(IMAGE) \
		-f $(THIS_FILE_DIR)/Dockerfile \
		$(THIS_FILE_DIR)/../source

run:
	docker run -d \
		--name $(CONTAINER) \
		--net $(NETWORK) \
		$(IMAGE)

stop:
	docker stop $(CONTAINER)


rm: stop
	docker rm $(CONTAINER)
