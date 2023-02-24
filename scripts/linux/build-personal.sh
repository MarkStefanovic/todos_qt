#!/bin/bash

SCRIPT_FOLDER=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LINUX_SCRIPTS_FOLDER="$(dirname "$SCRIPT_FOLDER")"
PROJECT_ROOT="$(dirname "$LINUX_SCRIPTS_FOLDER")"

echo "$PROJECT_ROOT"

rm -rf "$PROJECT_ROOT/dist/personal" \
&& mkdir "$PROJECT_ROOT/dist/personal" \
&& mkdir "$PROJECT_ROOT/dist/personal/assets" \
&& mkdir "$PROJECT_ROOT/dist/personal/assets/icons" \
&& cp "$PROJECT_ROOT/assets/secret/todosqt.desktop" "$PROJECT_ROOT/dist/personal/todosqt.desktop" \
&& cp -r "$PROJECT_ROOT/assets/icons" "$PROJECT_ROOT/dist/personal/assets/icons" \
&& conda run \
  -n todos-qt pyinstaller \
  "$PROJECT_ROOT/personal.spec" \
  --distpath "$PROJECT_ROOT/dist/personal" \
  --workpath "$PROJECT_ROOT/build"
