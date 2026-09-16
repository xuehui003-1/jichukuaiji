@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title 会计AI教学软件-环境诊断
echo 当前目录：%CD%
echo.
echo [Node]
where node.exe
node --version
echo.
echo [npm]
where npm.cmd
call npm.cmd --version
echo.
echo [关键文件]
if exist package.json (echo package.json: 正常) else (echo package.json: 缺失)
if exist node_modules (echo node_modules: 正常) else (echo node_modules: 缺失)
if exist node_modules\@prisma\client (echo Prisma Client: 正常) else (echo Prisma Client: 缺失)
if exist prisma\dev.db (echo SQLite数据库: 正常) else (echo SQLite数据库: 缺失)
echo.
echo 如有缺失，请先运行 setup-first-time.bat。
pause
