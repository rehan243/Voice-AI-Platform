#!/bin/bash

# this script sets up the development environment for the project

set -e  # exit immediately if a command exits with a non-zero status

# check for required tools
if ! command -v python3 &> /dev/null; then
    echo "python3 is required, please install it"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required, please install it"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "docker is required, please install it"
    exit 1
fi

# install required python packages
echo "installing required python packages..."
pip3 install -r requirements.txt

# build docker image
echo "building the docker image..."
docker build -t voice-ai-platform .

# run tests
echo "running tests..."
pytest tests/

# TODO: add linting step here
echo "running linters..."
flake8 src/

echo "development setup complete"