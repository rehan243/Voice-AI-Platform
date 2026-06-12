#!/bin/bash

# this script is for local development tasks
# linting and testing for the project

set -e  # exit immediately if a command exits with a non-zero status

# function to run linter
run_linter() {
    echo "running linter..."
    flake8 src/  # check the source files for style violations
    echo "linting completed"
}

# function to run tests
run_tests() {
    echo "running tests..."
    pytest tests/  # execute tests in the tests directory
    echo "all tests passed"
}

# main function to handle commands
main() {
    case "$1" in
        lint)
            run_linter
            ;;
        test)
            run_tests
            ;;
        all)
            run_linter
            run_tests
            ;;
        *)
            echo "usage: $0 {lint|test|all}"
            exit 1  # invalid argument
            ;;
    esac
}

# check if any arguments were provided
if [ "$#" -eq 0 ]; then
    echo "no command provided, running all tasks by default"
    main all
else
    main "$1"
fi

# TODO: add docker command options for better integration later