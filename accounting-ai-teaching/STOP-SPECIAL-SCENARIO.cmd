@echo off
setlocal EnableExtensions
echo Stopping local services on ports 2999, 3000 and 3001...
for %%P in (2999 3000 3001) do (
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":%%P " ^| findstr "LISTENING"') do taskkill /PID %%A /F >nul 2>nul
)
echo Scenario services stopped.
timeout /t 2 /nobreak >nul
