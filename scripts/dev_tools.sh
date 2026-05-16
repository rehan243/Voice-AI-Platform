#!/bin/bash

# this script is for running development tools like linting and testing

set -e  # exit immediately if a command exits with a non-zero status

# function to run flake8 for linting
run_lint() {
    echo "running flake8 for linting"
    flake8 src/ tests/
}

# function to run pytest for testing
run_tests() {
    echo "running pytest for tests"
    pytest tests/
}

# function to build and run docker container
run_docker() {
    echo "building and running docker container"
    docker-compose up --build
}

# checking for arguments
if [ "$#" -eq 0 ]; then
    echo "usage: $0 {lint|test|docker}"
    exit 1
fi

case "$1" in
    lint)
        run_lint
        ;;
    test)
        run_tests
        ;;
    docker)
        run_docker
        ;;
    *)
        echo "unknown command: $1"
        exit 1
        ;;
esac

# TODO: consider adding more commands for other dev tools
echo "done"