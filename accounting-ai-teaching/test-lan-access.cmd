@echo off
setlocal EnableExtensions
chcp 65001 >nul
set /p IP=Enter the laptop IPv4 address (example 192.168.0.107): 
echo.
echo Testing App A page...
curl.exe --max-time 5 -I http://%IP%:3000/
echo.
echo Testing App A session API...
curl.exe --max-time 5 http://%IP%:3000/api/auth/me
echo.
echo Testing App B page...
curl.exe --max-time 5 -I http://%IP%:3001/
echo.
echo Expected auth response when not logged in: {"ok":false}
echo If curl times out, check server windows and Windows Firewall Private network access.
pause
