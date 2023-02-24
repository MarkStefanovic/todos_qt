#!/bin/bash

SCRIPT_FOLDER=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LINUX_SCRIPTS_FOLDER="$(dirname "$SCRIPT_FOLDER")"
PROJECT_ROOT="$(dirname "$LINUX_SCRIPTS_FOLDER")"

conda env update --file "$PROJECT_ROOT/environment.yml"