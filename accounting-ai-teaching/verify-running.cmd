@echo off
setlocal EnableExtensions
chcp 65001 >nul
echo ========================================
echo Running system health checks
echo ========================================
echo.
echo [App A]
curl.exe -s --max-time 5 http://localhost:3000/api/health
echo.
echo.
echo [App B]
curl.exe -s --max-time 5 http://localhost:3001/api/health
echo.
echo.
echo Expected: "ok":true and "database":"connected" for both apps.
echo If AI mode is mock, configure DeepSeek only when online AI is needed.
pause
