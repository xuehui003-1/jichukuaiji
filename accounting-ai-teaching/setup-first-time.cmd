@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Accounting AI Teaching - First Setup

echo ========================================
echo Accounting AI Teaching - First Setup
echo ========================================
echo Project folder: %CD%
echo.

where node.exe >nul 2>nul
if errorlevel 1 goto NO_NODE
where npm.cmd >nul 2>nul
if errorlevel 1 goto NO_NODE

for /f "tokens=1 delims=." %%v in ('node.exe -p "process.versions.node"') do set NODE_MAJOR=%%v
echo Node version:
node.exe --version
echo npm version:
call npm.cmd --version
echo.

if %NODE_MAJOR% LSS 20 goto BAD_NODE
if %NODE_MAJOR% GTR 22 goto BAD_NODE

echo Preparing safe local configuration...
if not exist ".env" (
  >".env" echo DATABASE_URL="file:./dev.db"
  >>".env" echo AI_MODE="mock"
  >>".env" echo AI_BASE_URL="https://api.deepseek.com"
  >>".env" echo AI_MODEL="deepseek-v4-flash"
  >>".env" echo AI_API_KEY=""
)
if not exist "apps\life-ledger\.env.local" (
  >"apps\life-ledger\.env.local" echo DATABASE_URL="file:./dev.db"
  >>"apps\life-ledger\.env.local" echo AI_MODE="mock"
  >>"apps\life-ledger\.env.local" echo AI_BASE_URL="https://api.deepseek.com"
  >>"apps\life-ledger\.env.local" echo AI_MODEL="deepseek-v4-flash"
  >>"apps\life-ledger\.env.local" echo AI_API_KEY=""
  >>"apps\life-ledger\.env.local" echo NEXT_PUBLIC_APP_ID="LIFE_LEDGER"
)
if not exist "apps\payment-simulator\.env.local" (
  >"apps\payment-simulator\.env.local" echo DATABASE_URL="file:./dev.db"
  >>"apps\payment-simulator\.env.local" echo AI_MODE="mock"
  >>"apps\payment-simulator\.env.local" echo AI_BASE_URL="https://api.deepseek.com"
  >>"apps\payment-simulator\.env.local" echo AI_MODEL="deepseek-v4-flash"
  >>"apps\payment-simulator\.env.local" echo AI_API_KEY=""
  >>"apps\payment-simulator\.env.local" echo NEXT_PUBLIC_APP_ID="PAYMENT_SIMULATOR"
)
echo Safe local Mock configuration is ready.
echo.

echo [1/3] Installing dependencies...
echo Primary source: npm official registry and Prisma official engine server
call npm.cmd install
if not errorlevel 1 goto INSTALL_OK

echo.
echo --------------------------------------------------------
echo The first download failed. Retrying with China mirrors...
echo This usually fixes Prisma TLS/network disconnection errors.
echo --------------------------------------------------------
set "PRISMA_ENGINES_MIRROR=https://registry.npmmirror.com/-/binary/prisma"
set "npm_config_fetch_retries=5"
set "npm_config_fetch_retry_mintimeout=20000"
set "npm_config_fetch_retry_maxtimeout=120000"
call npm.cmd install --registry=https://registry.npmmirror.com
if errorlevel 1 goto NETWORK_FAILED

:INSTALL_OK
echo.
echo [2/3] Creating the local SQLite demo database...
call npm.cmd run db:setup
if errorlevel 1 goto FAILED

echo.
echo [3/3] Building production versions for stable LAN access...
call npm.cmd run build
if errorlevel 1 goto FAILED

echo.
echo ========================================
echo SETUP COMPLETED SUCCESSFULLY
echo Student: student_demo / demo1234
echo Teacher: teacher_demo / demo1234
echo ========================================
goto END

:NO_NODE
echo.
echo ERROR: Node.js or npm was not found.
echo Install Node.js 20 LTS or 22 LTS, then restart Windows.
goto END

:BAD_NODE
echo.
echo ERROR: Unsupported Node.js major version: %NODE_MAJOR%
echo This release supports Node.js 20 LTS or 22 LTS.
echo Node.js 23/24/25 are non-LTS or not validated for this package.
echo Please uninstall the current Node.js, install Node.js 22 LTS,
echo restart Windows, and run this script again.
goto END

:NETWORK_FAILED
echo.
echo ERROR: Dependency or Prisma engine download failed twice.
echo 1. Confirm the computer can open https://registry.npmmirror.com
echo 2. Temporarily disable HTTPS inspection/proxy software if permitted.
echo 3. Run repair-prisma-network.cmd after installing Node.js 20/22 LTS.
echo 4. Do not run from a restricted campus network; try a phone hotspot.
goto END

:FAILED
echo.
echo ERROR: Setup failed after dependency installation.
echo Please take a screenshot of the error messages above.
goto END

:END
echo.
echo Press any key to close this window...
pause >nul
endlocal
