@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Build App A Standalone Windows Package

if not exist "release" mkdir "release"
set "LOG=%CD%\release\portable-package-build.log"
>"%LOG%" echo [%date% %time%] Standalone portable package build started.

echo =============================================
echo Build App A Standalone Windows Package
echo =============================================
echo Output: %CD%\release
echo.

where node.exe >nul 2>nul
if errorlevel 1 goto NO_NODE
for /f "tokens=1 delims=." %%v in ('node.exe -p "process.versions.node"') do set NODE_MAJOR=%%v
if %NODE_MAJOR% LSS 20 goto BAD_NODE
if %NODE_MAJOR% GTR 22 goto BAD_NODE
for /f "delims=" %%i in ('where node.exe') do if not defined NODE_EXE set "NODE_EXE=%%i"

if not exist "node_modules\next\dist\bin\next" (
 echo Dependencies missing. Running npm install...
 call npm.cmd install >>"%LOG%" 2>&1
 if errorlevel 1 goto FAILED_INSTALL
)

if not exist "prisma\dev.db" (
 echo Demo database missing. Creating it...
 call npm.cmd run db:setup >>"%LOG%" 2>&1
 if errorlevel 1 goto FAILED_DB
)

echo [1/5] Building App A standalone production output...
call npm.cmd run build -w life-ledger >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_BUILD
if not exist "apps\life-ledger\.next\standalone\apps\life-ledger\server.js" goto FAILED_STANDALONE

set "OUT=%CD%\release\Accounting-AI-Teaching-AppA-Windows-Portable"
set "ZIP=%CD%\release\Accounting-AI-Teaching-AppA-Windows-Portable.zip"
if exist "%OUT%" rmdir /s /q "%OUT%"
if exist "%ZIP%" del /q "%ZIP%"
mkdir "%OUT%\runtime"
mkdir "%OUT%\standalone\apps\life-ledger\.next"
mkdir "%OUT%\standalone\apps\life-ledger\prisma"

echo [2/5] Copying portable Node runtime...
copy /y "%NODE_EXE%" "%OUT%\runtime\node.exe" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_COPY

echo [3/5] Copying standalone server and static assets...
robocopy "apps\life-ledger\.next\standalone" "%OUT%\standalone" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY
robocopy "apps\life-ledger\.next\static" "%OUT%\standalone\apps\life-ledger\.next\static" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY
robocopy "apps\life-ledger\public" "%OUT%\standalone\apps\life-ledger\public" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY

echo [4/5] Copying SQLite database and safe launcher...
copy /y "prisma\dev.db" "%OUT%\standalone\apps\life-ledger\prisma\dev.db" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_COPY
copy /y "prisma\dev.db" "%OUT%\standalone\node_modules\.prisma\client\dev.db" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_COPY
copy /y "scripts\portable-start-app-a.cmd" "%OUT%\START-APP-A.cmd" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_COPY
copy /y "scripts\portable-run-server.cmd" "%OUT%\RUN-SERVER.cmd" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_COPY

(
 echo ACCOUNTING AI TEACHING - APP A - WINDOWS PORTABLE PACKAGE
 echo.
 echo 1. Extract all files before running. Do not run inside the ZIP.
 echo 2. Double-click START-APP-A.cmd.
 echo 3. Keep the server window open.
 echo 4. The browser should open http://127.0.0.1:3000 automatically.
 echo 5. If not, manually enter http://127.0.0.1:3000.
 echo 6. Student: student_demo / demo1234
 echo 7. Teacher: teacher_demo / demo1234
 echo 8. This package uses Mock mode and contains no API key.
 echo 9. Stop: close the server window or press Ctrl+C.
 echo 10. Uninstall: stop the server and delete this folder.
)>"%OUT%\README-FIRST.txt"

echo [5/5] Creating ZIP. Please wait...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -LiteralPath '%OUT%' -DestinationPath '%ZIP%' -CompressionLevel Optimal -Force" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_ZIP

>>"%LOG%" echo [%date% %time%] SUCCESS: %ZIP%
echo.
echo PORTABLE PACKAGE CREATED SUCCESSFULLY
echo %ZIP%
start "" explorer.exe "%CD%\release"
goto END

:NO_NODE
set "ERR=Node.js not found. Install Node.js 22 LTS."
goto SHOW_ERROR
:BAD_NODE
set "ERR=Unsupported Node.js %NODE_MAJOR%. Use Node.js 20 or 22 LTS."
goto SHOW_ERROR
:FAILED_INSTALL
set "ERR=npm install failed."
goto SHOW_ERROR
:FAILED_DB
set "ERR=Database initialization failed."
goto SHOW_ERROR
:FAILED_BUILD
set "ERR=App A production build failed."
goto SHOW_ERROR
:FAILED_STANDALONE
set "ERR=Standalone server.js missing. Check next.config.ts output setting."
goto SHOW_ERROR
:FAILED_COPY
set "ERR=File copy failed."
goto SHOW_ERROR
:FAILED_ZIP
set "ERR=ZIP creation failed. Uncompressed folder may still work."
goto SHOW_ERROR
:SHOW_ERROR
echo ERROR: %ERR%
>>"%LOG%" echo [%date% %time%] ERROR: %ERR%
echo See: %LOG%
start "" explorer.exe "%CD%\release"
:END
echo.
echo Press any key to close...
pause >nul
endlocal
