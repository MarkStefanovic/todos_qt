@echo off
SET CurrentDirectory=%~dp0
for %%B in (%CurrentDirectory%.) do set ParentDirectory=%%~dpB
for %%B in (%ParentDirectory%.) do set GrandparentDirectory=%%~dpB
conda env update -f "%GrandparentDirectory%/environment.yml" --prune