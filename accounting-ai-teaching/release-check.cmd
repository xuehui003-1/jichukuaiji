@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title Accounting AI Teaching - Release Check
call npm.cmd run check:release
echo.
if errorlevel 1 (echo RELEASE CHECK FAILED) else (echo RELEASE CHECK PASSED)
pause
