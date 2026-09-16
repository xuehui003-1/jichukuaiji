@echo off
setlocal
cd /d "%~dp0standalone\apps\life-ledger"
set "PORT=3000"
set "HOSTNAME=127.0.0.1"
set "DATABASE_URL=file:./dev.db"
set "AI_MODE=mock"
title App A Server - Keep This Window Open

echo =============================================
echo Accounting AI Teaching App A
echo =============================================
echo Keep this server window open while using App A.
echo Browser address: http://127.0.0.1:3000
echo.

"%~dp0runtime\node.exe" server.js

echo.
echo App A has stopped. Press any key to close.
pause >nul
endlocal
