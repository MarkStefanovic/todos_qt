echo Updating todos-qt env...

cd %~dp0

cd ../..

hatch run pip-compile --upgrade

hatch run python -m pip_audit --fix

echo Finished updating todos-qt env.
