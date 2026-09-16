@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo LAN access addresses
echo Keep this laptop and the other computer on the same Wi-Fi/LAN.
echo Keep both app server windows open.
echo ========================================
echo.
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4"') do (
  set IP=%%A
  call :SHOW
)
echo If Windows asks about firewall access, allow Node.js on Private networks.
pause
exit /b
:SHOW
set IP=%IP: =%
echo App A: http://%IP%:3000
echo App B: http://%IP%:3001
echo.
exit /b
