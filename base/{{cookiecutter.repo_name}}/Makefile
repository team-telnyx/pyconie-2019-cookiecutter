# Makefile for {{cookiecutter.app_name}} Service

# VARIABLES

# Change these variables.
service := {{cookiecutter.container_name}}
tag := $(or ${BUILD_NUMBER},dev)

python_version := 3.6
pip_version := 18.1
pipenv_version := 2018.11.26
black_version := 18.9b0

# Generated variables.
main_image := registry:5000/jenkins/$(service):$(tag)
docker_build_args = \
	--build-arg GIT_COMMIT=$(shell git show -s --format=%H) \
	--build-arg GIT_COMMIT_DATE="$(shell git show -s --format=%ci)" \
	--build-arg IMAGE_NAME=$(service) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%T.%N%Z") \
	--build-arg BUILD_URL=$(BUILD_URL) \
	--build-arg VER_PYTHON=$(python_version) \
	--build-arg VER_PIP=$(pip_version) \
	--build-arg VER_PIPENV=$(pipenv_version)

# TARGETS

.PHONY: all clean test deps run integrate push build lockdeps

all: build

clean:
	docker rmi -f $(main_image)

# Nomad currently expects to be able to run a test against a container, so we'll point test to integrate
test: integrate

# The original cookie cutter has a test target, but we had to hijack it for Nomad.  This is what used to be test.
test_local:
	invoke test

deps:
	pipenv install

run:
	docker-compose -p {{cookiecutter.repo_name}} build {{cookiecutter.container_name}}
	docker-compose -p {{cookiecutter.repo_name}} up {{cookiecutter.container_name}}

integrate: build
	docker-compose -p {{cookiecutter.container_name}}-ci run -e TAG=$(tag) --rm ci

push:
	docker push $(main_image)

build:
	docker build $(docker_build_args) -t $(main_image) .

black:
	pipenv run black .

# these are convoluted, but work without needing much installed locally.
pipenv-lock-depfree:
	docker run \
		--rm \
		--workdir /app \
		--volume $(shell pwd):/app \
		python:$(python_version)-alpine \
		sh -c "pip3 install pipenv==$(pipenv_version) && pipenv lock --verbose"

black-depfree:
	docker run \
		--rm \
		--workdir /app \
		--volume $(shell pwd):/app \
		python:$(python_version)-alpine \
		sh -c "pip3 install black==$(black_version) && black ."
