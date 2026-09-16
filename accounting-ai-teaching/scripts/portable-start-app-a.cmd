@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title App A One-Click Launcher
set "HEALTH_FILE=%TEMP%\app-a-health-%RANDOM%.txt"

echo Starting App A server...
start "App A Server - Keep Open" "%~dp0RUN-SERVER.cmd"

echo Waiting for the application and database to become ready...
for /L %%i in (1,1,40) do (
  curl.exe -fsS --max-time 1 "http://127.0.0.1:3000/api/health" >"%HEALTH_FILE%" 2>nul
  findstr /C:"\"ok\":true" "%HEALTH_FILE%" >nul 2>nul
  if not errorlevel 1 (
    findstr /C:"\"database\":\"connected\"" "%HEALTH_FILE%" >nul 2>nul
    if not errorlevel 1 goto READY
  )
  timeout /t 1 /nobreak >nul
)

echo.
echo App A did not become ready within 40 seconds.
echo Check the separate App A Server window for errors.
if exist "%HEALTH_FILE%" del /q "%HEALTH_FILE%"
echo Press any key to close this launcher.
pause >nul
goto END

:READY
if exist "%HEALTH_FILE%" del /q "%HEALTH_FILE%"
echo App A is ready. Opening the login page...
start "" "http://127.0.0.1:3000"
timeout /t 2 /nobreak >nul

:END
endlocal
