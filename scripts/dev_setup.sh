#!/bin/bash

# this script sets up the development environment for the voice ai platform

set -e  # exit on error

# check if docker is installed
if ! command -v docker &> /dev/null
then
    echo "docker not found, please install it first"
    exit 1
fi

# run docker compose to set up services
echo "starting up services with docker compose..."
docker-compose up -d

# run linter
echo "running linter..."
if ! flake8 src/; then
    echo "linting issues found, please fix them"
    exit 1
fi

# run tests
echo "running tests..."
if ! pytest tests/; then
    echo "some tests failed, check the output above"
    exit 1
fi

# TODO: add coverage report generation

echo "development setup is complete"