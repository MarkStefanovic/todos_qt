@ECHO OFF & SETLOCAL
for %%i in ("%~dp0..") DO SET "folder=%%~fi"
@ECHO ON
del /S /Q "%folder%\dist\"
conda run -n todos-qt pyinstaller "%folder%\app.spec" --distpath %folder%\dist\ --specpath %folder% --workpath %folder%\build
