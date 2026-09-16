@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Accounting AI Teaching - Diagnostics
echo Project folder: %CD%
echo.
echo [Node]
where node.exe
node.exe --version
echo.
echo [npm]
where npm.cmd
call npm.cmd --version
echo.
echo [Files]
if exist package.json (echo package.json: OK) else (echo package.json: MISSING)
if exist node_modules (echo node_modules: OK) else (echo node_modules: MISSING)
if exist node_modules\@prisma\client (echo Prisma Client: OK) else (echo Prisma Client: MISSING)
if exist prisma\dev.db (echo SQLite database: OK) else (echo SQLite database: MISSING)
echo.
pause
