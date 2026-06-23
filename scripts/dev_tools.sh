#!/bin/bash

# this script is for setting up local dev tools
# make sure to give it execute permissions with chmod +x scripts/dev_tools.sh

echo "starting development tools setup..."

# check for required tools
if ! command -v flake8 &> /dev/null; then
    echo "flake8 not found, installing..."
    pip install flake8
fi

if ! command -v pytest &> /dev/null; then
    echo "pytest not found, installing..."
    pip install pytest
fi

# run linter
echo "running linter..."
flake8 src/ > lint_report.txt

if [ $? -eq 0 ]; then
    echo "linting passed, no issues found"
else
    echo "linting issues found, check lint_report.txt"
fi

# run tests
echo "running tests..."
pytest tests/ > test_report.txt

if [ $? -eq 0 ]; then
    echo "all tests passed!"
else
    echo "some tests failed, see test_report.txt for details"
fi

# TODO: add docker support to build and run the app locally

echo "development tools setup complete!"