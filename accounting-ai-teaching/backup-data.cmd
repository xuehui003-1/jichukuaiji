@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "prisma\dev.db" goto NODB
if not exist backups mkdir backups
for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%T
copy /y "prisma\dev.db" "backups\dev_%TS%.db" >nul
echo Backup created: backups\dev_%TS%.db
pause
exit /b 0
:NODB
echo SQLite database was not found.
pause
