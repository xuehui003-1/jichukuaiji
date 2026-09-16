@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title 会计AI教学软件-首次安装

echo ========================================
echo   会计AI教学软件 - 首次安装
echo ========================================
echo 当前目录：%CD%
echo.
where node.exe >nul 2>nul
if errorlevel 1 goto nonode
where npm.cmd >nul 2>nul
if errorlevel 1 goto nonode

echo Node版本：
node --version
echo npm版本：
call npm.cmd --version
echo.
echo [1/2] 正在安装项目依赖，请耐心等待...
call npm.cmd install
if errorlevel 1 goto error

echo.
echo [2/2] 正在初始化本机SQLite演示数据库...
call npm.cmd run db:setup
if errorlevel 1 goto error

echo.
echo ========================================
echo 首次安装完成！
echo 以后直接双击 start-app-a.bat 或 start-app-b.bat。
echo 演示账号：student_demo / teacher_demo
echo 演示密码：demo1234
echo ========================================
pause
exit /b 0

:nonode
echo.
echo 未检测到Node.js或npm。请先安装Node.js 20以上版本，安装后重启电脑。
pause
exit /b 1

:error
echo.
echo 安装失败。请不要关闭窗口，截图上方红色或npm错误信息。
pause
exit /b 1
