@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Repair Prisma Network Download

echo ========================================
echo Repair Prisma Engine Download
echo ========================================
echo This script uses the npmmirror Prisma binary mirror.
echo It does not change application data.
echo.

where node.exe >nul 2>nul
if errorlevel 1 goto NO_NODE
for /f "tokens=1 delims=." %%v in ('node.exe -p "process.versions.node"') do set NODE_MAJOR=%%v
if %NODE_MAJOR% LSS 20 goto BAD_NODE
if %NODE_MAJOR% GTR 22 goto BAD_NODE

set "PRISMA_ENGINES_MIRROR=https://registry.npmmirror.com/-/binary/prisma"
set "npm_config_fetch_retries=5"
set "npm_config_fetch_retry_mintimeout=20000"
set "npm_config_fetch_retry_maxtimeout=120000"

echo [1/2] Installing dependencies with mirror...
call npm.cmd install --registry=https://registry.npmmirror.com
if errorlevel 1 goto FAILED

echo [2/2] Generating Prisma Client...
call npm.cmd run db:generate
if errorlevel 1 goto FAILED

echo.
echo REPAIR COMPLETED. Now run setup-first-time.cmd again.
goto END

:NO_NODE
echo ERROR: Node.js not found. Install Node.js 22 LTS first.
goto END

:BAD_NODE
echo ERROR: Please use Node.js 20 LTS or 22 LTS. Current major: %NODE_MAJOR%
goto END

:FAILED
echo.
echo REPAIR FAILED.
echo Try a phone hotspot or another unrestricted network.
goto END

:END
echo.
pause
endlocal
