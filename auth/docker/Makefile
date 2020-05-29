IMAGE = jwt_auth_issuer
CONTAINER = jwt-auth
NETWORK = kong-net

THIS_FILE := $(realpath $(lastword $(MAKEFILE_LIST)))
THIS_FILE_DIR := $(shell dirname $(THIS_FILE))

build:
	DOCKER_BUILDKIT=1 docker build \
		-t $(IMAGE) \
		-f $(THIS_FILE_DIR)/Dockerfile \
		$(THIS_FILE_DIR)/../source

setup:
	openssl genrsa -out $(THIS_FILE_DIR)/../source/resources/private.pem 2048

run:
	docker run -d \
		--name $(CONTAINER) \
		-p 5000:5000 \
		--net $(NETWORK) \
		$(IMAGE)

stop:
	docker stop $(CONTAINER)


rm: stop
	docker rm $(CONTAINER)
