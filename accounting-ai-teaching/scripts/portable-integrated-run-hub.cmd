@echo off
setlocal
cd /d "%~dp0services\hub\apps\ai-finance-hub"
set "PORT=2999"
set "HOSTNAME=127.0.0.1"
set "DATABASE_URL=file:../../../../database/dev.db"
set "AI_MODE=mock"
title Accounting Intelligent Learning Hub - Keep Open
"%~dp0runtime\node.exe" server.js
