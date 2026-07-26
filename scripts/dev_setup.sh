#!/bin/bash

# this script sets up the development environment

# check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "docker is not running. please start docker first."
    exit 1
fi

# install python dependencies
echo "installing python dependencies..."
pip install -r requirements.txt

# check for linting issues
echo "running linters..."
flake8 src/ --max-line-length=88
if [ $? -ne 0 ]; then
    echo "linting errors found. please fix them."
    exit 1
fi

# run tests
echo "running tests..."
pytest tests/
if [ $? -ne 0 ]; then
    echo "some tests failed. please check the output above."
    exit 1
fi

# build docker image
echo "building docker image..."
docker build -t voice-ai-platform .

# optional: run the container
read -p "do you want to run the docker container? (y/n) " run_container
if [[ "$run_container" == "y" ]]; then
    docker run -p 5000:5000 voice-ai-platform
fi

echo "dev environment setup complete!"