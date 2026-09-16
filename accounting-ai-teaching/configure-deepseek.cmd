@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Configure DeepSeek API
set /p API_KEY=Paste your DeepSeek API Key and press Enter: 
if "%API_KEY%"=="" goto EMPTY
(
echo DATABASE_URL="file:./dev.db"
echo AI_MODE="online"
echo AI_BASE_URL="https://api.deepseek.com"
echo AI_MODEL="deepseek-v4-flash"
echo AI_API_KEY="%API_KEY%"
echo NEXT_PUBLIC_APP_ID="LIFE_LEDGER"
)>apps\life-ledger\.env.local
(
echo DATABASE_URL="file:./dev.db"
echo AI_MODE="online"
echo AI_BASE_URL="https://api.deepseek.com"
echo AI_MODEL="deepseek-v4-flash"
echo AI_API_KEY="%API_KEY%"
echo NEXT_PUBLIC_APP_ID="PAYMENT_SIMULATOR"
)>apps\payment-simulator\.env.local
echo DeepSeek configuration saved for both apps.
echo Restart both app servers to apply it.
goto END
:EMPTY
echo No key entered. Nothing changed.
:END
pause
