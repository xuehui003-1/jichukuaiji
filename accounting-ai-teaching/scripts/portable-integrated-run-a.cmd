@echo off
setlocal
cd /d "%~dp0services\a\apps\life-ledger"
set "PORT=3000"
set "HOSTNAME=127.0.0.1"
set "DATABASE_URL=file:../../../../database/dev.db"
set "AI_MODE=mock"
title Life Event Intelligent Analysis - Keep Open
"%~dp0runtime\node.exe" server.js
