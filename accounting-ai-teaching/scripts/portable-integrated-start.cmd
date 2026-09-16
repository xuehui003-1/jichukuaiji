@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Accounting Intelligent Learning Platform
echo ===============================================
echo Accounting Intelligent Learning Platform
echo Five-link integrated offline package
echo ===============================================
if not exist "runtime\node.exe" goto NOT_READY
if not exist "database\dev.db" goto NOT_READY
start "Life Analysis Server" /D "%~dp0" cmd.exe /d /k "RUN-A.cmd"
timeout /t 2 /nobreak >nul
start "Payment Simulation Server" /D "%~dp0" cmd.exe /d /k "RUN-B.cmd"
timeout /t 2 /nobreak >nul
start "Five-link Hub Server" /D "%~dp0" cmd.exe /d /k "RUN-HUB.cmd"
echo Waiting for local services...
for /l %%I in (1,1,40) do (
  curl.exe -s --max-time 1 http://127.0.0.1:2999/api/status | findstr /c:"\"appA\":true" | findstr /c:"\"appB\":true" >nul && goto READY
  timeout /t 1 /nobreak >nul
)
echo Services are still starting. Opening the platform now.
goto OPEN
:READY
echo All services are ready.
:OPEN
start "" "http://127.0.0.1:2999"
exit /b 0
:NOT_READY
echo ERROR: Portable package files are incomplete.
echo Please extract the complete ZIP before running.
pause
