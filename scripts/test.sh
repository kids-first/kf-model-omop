#!/bin/bash

source ./venv/bin/activate
py.test --pep8 src
py.test --cov=src tests
