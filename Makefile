# this Makefile is for building and managing our voice ai platform
.PHONY: lint test docker run

# linting with flake8
lint:
	@echo "running flake8 for linting"
	flake8 src/

# running tests with pytest
test:
	@echo "running tests with pytest"
	pytest tests/

# build docker image
docker:
	@echo "building the docker image"
	docker build -t voice-ai-platform .

# run the application locally
run:
	@echo "starting the application locally"
	python src/main.py

# todo: add more targets as needed