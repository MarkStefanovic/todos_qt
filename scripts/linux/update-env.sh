#!/bin/bash

echo updating todos-qt env...

hatch run pip-compile --upgrade

hatch run python -m pip_audit --fix

echo todos-qt env updated.