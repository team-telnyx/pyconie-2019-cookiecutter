tools-container-tag := cookiecutter-tools
runs-with-tools := \
	docker run \
		--rm \
		--user $(shell id -u):$(shell id -g) \
		--workdir /app \
		--volume $(shell pwd):/app \
		$(tools-container-tag)

target := example-project

.PHONY: clean
clean:
	rm -rf $(target)

.PHONY: tools
tools:
	docker build --tag $(tools-container-tag) --file tools.Dockerfile .

.PHONY: stockstamp
stockstamp: tools
	$(runs-with-tools) cookiecutter --no-input .
	$(runs-with-tools) black $(target)

.PHONY: stamp
stamp: tools
	$(runs-with-tools) cookiecutter .

.PHONY: lockdeps
lockdeps: tools
	$(runs-with-tools) sh -c "cd $(target) && pipenv lock --verbose"

.PHONY: test
test:
	./test.sh
