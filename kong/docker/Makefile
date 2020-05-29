SHELL := /bin/bash
IMAGE = kong:2.0
CONTAINER = kong
NETWORK = kong-net

KONG_DB = kong-database

THIS_FILE := $(realpath $(lastword $(MAKEFILE_LIST)))
THIS_FILE_DIR := $(shell dirname $(THIS_FILE))

# service conf
API_NAME = flask-api
PUBKEY_PATH = $(THIS_FILE_DIR)/../source/resources/public.pem


build:
	DOCKER_BUILDKIT=1 docker build -f $(THIS_FILE_DIR)/Dockerfile \
		-t $(IMAGE) \
		$(THIS_FILE_DIR)/../source

setup:
	@echo Generating Pubkey from $(PRIVKEY_PATH)
	openssl rsa -in $(PRIVKEY_PATH) -outform PEM \
		-pubout -out $(PUBKEY_PATH)


run:
	docker run -d \
		--name ${CONTAINER} \
		--net ${NETWORK} \
		--env-file $(THIS_FILE_DIR)/../source/resources/kong.env \
		-e KONG_PG_HOST=$(KONG_DB) \
		-p 8003:8000 \
		-p 8443:8443 \
		-p 8001:8001 \
		-p 8444:8444 \
		${IMAGE}


init_db:
	docker run --rm \
		--net $(NETWORK) \
		-e KONG_DATABASE=postgres \
		-e KONG_PG_HOST=$(KONG_DB) \
		$(IMAGE) kong migrations bootstrap


init_api:
	curl -i -X POST http://localhost:8001/services \
		--data name=flask-api \
		--data url='http://flask-api:5000' 
	curl -i http://localhost:8001/services/$(API_NAME)


add_routes:
	curl -i -X POST http://localhost:8001/services/$(API_NAME)/routes \
		--data 'paths[]=/hello' \
		--data 'name=hello' \
		--data 'strip_path=false'
	curl -i -X POST http://localhost:8001/services/$(API_NAME)/routes \
		--data 'paths[]=/secret' \
		--data 'name=secret' \
		--data 'strip_path=false'

register_api: init_api add_routes

test_routes:
	curl -i http://localhost:8003/hello
	curl -i http://localhost:8003/secret

test_routes_auth:
	$(eval token:=$(shell curl -s -F user=admin -F password=admin localhost:5000/auth | jq -r '.access_token'))
	curl -i http://localhost:8003/hello
	curl -i -H "Authorization: Bearer $(token)" http://localhost:8003/secret

add_consumer:
	curl -i -X POST localhost:8001/consumers --data username=api

add_jwt:
	curl -i -X POST localhost:8001/consumers/api/jwt \
        -F 'algorithm=RS256' \
		-F 'key=kong-auth' \
		-F 'rsa_public_key=@$(PUBKEY_PATH)'


secure_route:
	curl -i -X POST localhost:8001/routes/secret/plugins \
		--data "name=jwt" \
		--data "config.claims_to_verify=exp"

secure_api: add_consumer add_jwt secure_route


rm_routes:
	curl -i -X DELETE http://localhost:8001/services/$(API_NAME)/routes/hello
	curl -i -X DELETE http://localhost:8001/services/$(API_NAME)/routes/secret

rm_api:
	curl -i -X DELETE http://localhost:8001/services/$(API_NAME)
	

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
