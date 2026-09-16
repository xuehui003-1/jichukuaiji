@echo off
setlocal
cd /d "%~dp0"
if not exist backups mkdir backups
echo Available database backups:
dir /b /o-d backups\*.db 2>nul
echo.
echo To restore, close both app servers, then copy a selected backup file over prisma\dev.db.
pause
