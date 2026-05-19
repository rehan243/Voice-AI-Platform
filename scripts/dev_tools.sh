#!/bin/bash

# this script is for development tasks like linting and testing

set -e  # exit immediately if a command exits with a non-zero status

# check if dependencies are installed
check_dependencies() {
    command -v flake8 >/dev/null 2>&1 || { echo "flake8 is not installed. Aborting." >&2; exit 1; }
    command -v pytest >/dev/null 2>&1 || { echo "pytest is not installed. Aborting." >&2; exit 1; }
}

# run linter
run_linter() {
    echo "running linter..."
    flake8 src/  # assuming the source code is under src/
}

# run tests
run_tests() {
    echo "running tests..."
    pytest tests/  # assuming test files are under tests/
}

# build docker image
build_docker_image() {
    echo "building docker image..."
    docker build -t voice-ai-platform .  # build the docker image
}

# main function
main() {
    check_dependencies  # check if all necessary tools are installed
    run_linter  # lint the code
    run_tests  # run the test suite
    build_docker_image  # build the docker image
}

# execute the main function
main