#!/bin/bash

echo "Running flake8..."
flake8 --ignore=E501 webapp/*.py
echo

echo "Running pylint..."
pylint --disable=line-too-long,missing-module-docstring webapp/*.py
echo
