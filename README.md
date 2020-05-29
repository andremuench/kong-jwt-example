# Securing API with Kong and JWT

Example of how to secure an API (dynamically) with Kong and JWT. All modules are dockerized. All modules are managed with Makefiles. Please find details below.

## Modules

### API

Simple API written in Flask with two directives: `/hello` and `/secure` . The latter is the directive which is to be secured. Listening on port 5000, not exposed.

```
|
\- /hello    
\- /secure 
```

#### Manage

````bash
# build docker container
make build
# run the container
make run
# stop and remove the container
make rm
````

### Auth

The token issuer written in Flask. Assymetric crypto is used. Tokens can be retrieved by the directive `/auth` 

#### Manage

```bash
# generate private key
make setup
# build docker container
make build
# run the container
make run
# stop and remove the container
make rm
```

#### Usage

```bash
curl -i -F user=admin -F password=admin localhost:5000/auth
```

```js
{ "access_token": "eyJhbGciOiJSUzI1NiI..."}
```

### Kong

The kong microservice to expose the api with a secured route and configured to use the Postgres database

#### Manage

```bash
# generate public key
make setup
# build docker container
make build
# initialize db
make init_db
# run the container
make run
# stop and remove the container
make rm
```

#### Usage/Testing

````bash
# register api and routes
make register_api
# secure api route /secure
make secure_api
# call the api without authorization
make test_routes
# call the api with authorization
make test_routes_auth
````

### Kong DB

A plain postgres database

#### Manage

```bash
# build docker container
make build
# run the container
make run
# stop and remove the container
make rm
```

