#!/bin/bash

SCRIPT_FOLDER=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LINUX_SCRIPTS_FOLDER="$(dirname "$SCRIPT_FOLDER")"
PROJECT_ROOT="$(dirname "$LINUX_SCRIPTS_FOLDER")"

conda env update --file "$PROJECT_ROOT/environment.yml"

call conda run -n todos-qt python -m pip_audit --fix

pip install -v --ignore-requires-python "pyqtdarktheme>=2.1.0"
#pip install --force-reinstall -v --ignore-requires-python "pyqtdarktheme>=2.1.0"

echo todos-qt env updated.