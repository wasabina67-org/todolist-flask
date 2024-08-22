#!/bin/bash

isort src/*.py
black src/*.py
flake8 src/*.py
mypy src/*.py
