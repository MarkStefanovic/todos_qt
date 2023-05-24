#!/bin/bash

SCRIPT_FOLDER=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LINUX_SCRIPTS_FOLDER="$(dirname "$SCRIPT_FOLDER")"
PROJECT_ROOT="$(dirname "$LINUX_SCRIPTS_FOLDER")"

echo "$PROJECT_ROOT"

rm -rf "$PROJECT_ROOT/dist/" \
&& mkdir "$PROJECT_ROOT/dist/" \
&& mkdir "$PROJECT_ROOT/dist/personal/" \
&& cp -r "$PROJECT_ROOT/assets/" "$PROJECT_ROOT/dist/personal/" \
&& conda run \
  -n todos-qt \
  pyinstaller \
  "$PROJECT_ROOT/personal.spec" \
  --distpath "$PROJECT_ROOT/dist/personal" \
  --workpath "$PROJECT_ROOT/build"
