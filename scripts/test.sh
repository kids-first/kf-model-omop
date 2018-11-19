#!/bin/bash

source ./venv/bin/activate
py.test --pep8 kf_model_omop
py.test --cov=kf_model_omop tests
