#!/bin/bash

isort src/*.py
black src/*.py
flake8 src/*.py
mypy src/*.py

isort tests/*.py
black tests/*.py
flake8 tests/*.py
mypy tests/*.py
