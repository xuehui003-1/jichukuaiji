@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 警告：该操作会删除本机测试数据并恢复匿名演示数据。
choice /c YN /m "确定继续吗"
if errorlevel 2 exit /b 0
call npm run db:setup
pause
