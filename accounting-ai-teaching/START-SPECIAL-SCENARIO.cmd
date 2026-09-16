@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title AI Finance Integrated Scenario Launcher
if not exist "node_modules\@prisma\client" goto NOT_READY
if not exist "prisma\dev.db" goto NOT_READY
if not exist "apps\life-ledger\.next\BUILD_ID" goto NOT_READY
if not exist "apps\payment-simulator\.next\BUILD_ID" goto NOT_READY
if not exist "apps\ai-finance-hub\.next\BUILD_ID" goto NOT_READY
echo ===============================================
echo AI Finance Integrated Teaching Scenario
echo ===============================================
echo [1/3] Starting App A on port 3000...
start "App A - Life Ledger" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:a"
timeout /t 2 /nobreak >nul
echo [2/3] Starting App B on port 3001...
start "App B - Payment Simulator" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:b"
timeout /t 2 /nobreak >nul
echo [3/3] Starting Scenario Hub on port 2999...
start "Scenario Hub" /D "%~dp0" cmd.exe /d /k "npm.cmd run serve:hub"
echo Waiting for all health checks...
for /l %%I in (1,1,35) do (
  curl.exe -s --max-time 1 http://127.0.0.1:2999/api/status | findstr /c:"\"appA\":true" | findstr /c:"\"appB\":true" >nul && goto READY
  timeout /t 1 /nobreak >nul
)
echo One or more services may still be starting.
echo Opening the hub; use its status refresh button to check again.
goto OPEN
:READY
echo All three services are ready.
:OPEN
start "" "http://127.0.0.1:2999"
exit /b 0
:NOT_READY
echo The project is not fully installed or built.
echo Run setup-first-time.cmd first, then run this launcher again.
pause
exit /b 1
