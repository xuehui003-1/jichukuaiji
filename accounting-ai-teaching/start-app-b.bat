@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
where npm.cmd >nul 2>nul
if errorlevel 1 goto nonode
if not exist "node_modules\@prisma\client" goto notinstalled
if not exist "prisma\dev.db" goto notinstalled

echo 正在启动应用B，请保留服务器窗口...
start "应用B服务器-关闭此窗口即可停止" /D "%~dp0" cmd.exe /k "npm.cmd run dev:b"
timeout /t 4 /nobreak >nul
start "" "http://localhost:3001"
exit /b 0

:notinstalled
echo 尚未完成依赖或数据库初始化，请先双击 setup-first-time.bat。
pause
exit /b 1
:nonode
echo 未检测到npm，请确认Node.js已安装并重启电脑。
pause
exit /b 1
