@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "node_modules\@prisma\client" goto NOT_READY
if not exist "prisma\dev.db" goto NOT_READY
if not exist "apps\life-ledger\.next\BUILD_ID" goto NOT_READY
echo Starting App A...
start "App A Server" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:a"
echo Waiting for the health check...
for /l %%I in (1,1,25) do (
  curl.exe -s --max-time 1 http://localhost:3000/api/health | findstr /c:"\"ok\":true" >nul && goto READY
  timeout /t 1 /nobreak >nul
)
echo Server did not become ready in 25 seconds.
echo Check the server window for errors.
pause
exit /b 1
:READY
echo App A is ready: http://localhost:3000
start "" "http://localhost:3000"
exit /b 0
:NOT_READY
echo Project is not initialized or built. Run setup-first-time.cmd first.
pause
