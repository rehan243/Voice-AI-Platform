#!/bin/bash

# check if docker is installed
if ! command -v docker &> /dev/null
then
    echo "docker could not be found, please install it first"
    exit 1
fi

# check if python is installed
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found, please install it first"
    exit 1
fi

# install dependencies
echo "installing dependencies"
pip install -r requirements.txt

# run linting
echo "running flake8 for linting"
flake8 src/

# run tests
echo "running tests with pytest"
pytest tests/

# build docker image
echo "building docker image"
docker build -t voice-ai-platform .

# run the docker container
echo "running docker container"
docker run -it --rm voice-ai-platform

# TODO: add more commands as needed

echo "development setup complete"