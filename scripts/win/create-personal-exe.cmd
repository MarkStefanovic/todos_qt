@echo off
SET CurrentDirectory=%~dp0
for %%B in (%CurrentDirectory%.) do set ParentDirectory=%%~dpB
for %%B in (%ParentDirectory%.) do set GrandparentDirectory=%%~dpB
cd "%GrandparentDirectory%"
del /S /Q "%GrandparentDirectory%\dist\"
xcopy %GrandparentDirectory%\assets\icons %GrandparentDirectory%\dist\assets\icons /s /e
conda run -n todos-qt pyinstaller "%GrandparentDirectory%personal.spec"
