@echo off
setlocal EnableExtensions
cd /d "%~dp0"
(
echo DATABASE_URL="file:./dev.db"
echo AI_MODE="mock"
echo AI_BASE_URL="https://api.deepseek.com"
echo AI_MODEL="deepseek-v4-flash"
echo AI_API_KEY=""
echo NEXT_PUBLIC_APP_ID="LIFE_LEDGER"
)>apps\life-ledger\.env.local
(
echo DATABASE_URL="file:./dev.db"
echo AI_MODE="mock"
echo AI_BASE_URL="https://api.deepseek.com"
echo AI_MODEL="deepseek-v4-flash"
echo AI_API_KEY=""
echo NEXT_PUBLIC_APP_ID="PAYMENT_SIMULATOR"
)>apps\payment-simulator\.env.local
echo Both apps now use offline Mock AI. Restart app servers.
pause
