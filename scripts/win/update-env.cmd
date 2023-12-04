@echo off
SET CurrentDirectory=%~dp0
for %%B in (%CurrentDirectory%.) do set ParentDirectory=%%~dpB
for %%B in (%ParentDirectory%.) do set GrandparentDirectory=%%~dpB

call conda env update -f "%GrandparentDirectory%/environment.yml" --prune

call conda run -n todos-qt python -m pip_audit --fix

echo Finished updating todos-qt env.
