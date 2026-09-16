@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "node_modules\@prisma\client" goto NOT_READY
if not exist "prisma\dev.db" goto NOT_READY
if not exist "apps\life-ledger\.next\BUILD_ID" goto NOT_READY
if not exist "apps\payment-simulator\.next\BUILD_ID" goto NOT_READY
echo Starting App A and App B...
start "App A Server" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:a"
timeout /t 2 /nobreak >nul
start "App B Server" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:b"
timeout /t 5 /nobreak >nul
start "" "http://localhost:3000"
start "" "http://localhost:3001"
exit /b 0
:NOT_READY
echo Project is not fully initialized or built.
echo Run setup-first-time.cmd first.
pause
