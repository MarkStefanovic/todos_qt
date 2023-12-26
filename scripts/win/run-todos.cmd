@echo off
SET CurrentDirectory=%~dp0
for %%B in (%CurrentDirectory%.) do set ParentDirectory=%%~dpB
for %%B in (%ParentDirectory%.) do set GrandparentDirectory=%%~dpB
cd "%GrandparentDirectory%"
::start conda run -n todos-qt --live-stream python -m src.main
::exit 0


C:\hatch\hatch.exe run python -m src.main