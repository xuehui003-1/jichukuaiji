@echo off
setlocal
cd /d "%~dp0services\b\apps\payment-simulator"
set "PORT=3001"
set "HOSTNAME=127.0.0.1"
set "DATABASE_URL=file:../../../../database/dev.db"
set "AI_MODE=mock"
title Digital Payment Relationship Simulation - Keep Open
"%~dp0runtime\node.exe" server.js
