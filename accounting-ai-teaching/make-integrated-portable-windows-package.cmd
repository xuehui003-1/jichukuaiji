@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Build Five-link Integrated Windows Portable Package
if not exist release mkdir release
set "LOG=%CD%\release\integrated-portable-build.log"
>"%LOG%" echo [%date% %time%] Build started.
where node.exe >nul 2>nul || goto NO_NODE
for /f "delims=" %%i in ('where node.exe') do if not defined NODE_EXE set "NODE_EXE=%%i"
if not exist "node_modules\next\dist\bin\next" goto NOT_READY
if not exist "prisma\dev.db" goto NOT_READY
echo [1/7] Building all three standalone services...
call npm.cmd run build >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_BUILD
for %%F in ("apps\life-ledger\.next\standalone\apps\life-ledger\server.js" "apps\payment-simulator\.next\standalone\apps\payment-simulator\server.js" "apps\ai-finance-hub\.next\standalone\apps\ai-finance-hub\server.js") do if not exist %%F goto FAILED_STANDALONE
set "OUT=%CD%\release\Accounting-Five-Link-Windows-Portable"
set "ZIP=%CD%\release\Accounting-Five-Link-Windows-Portable.zip"
if exist "%OUT%" rmdir /s /q "%OUT%"
if exist "%ZIP%" del /q "%ZIP%"
mkdir "%OUT%\runtime" "%OUT%\database" "%OUT%\services\a" "%OUT%\services\b" "%OUT%\services\hub"
echo [2/7] Copying portable Node runtime...
copy /y "%NODE_EXE%" "%OUT%\runtime\node.exe" >>"%LOG%" 2>&1 || goto FAILED_COPY
echo [3/7] Copying standalone services...
robocopy "apps\life-ledger\.next\standalone" "%OUT%\services\a" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY
robocopy "apps\payment-simulator\.next\standalone" "%OUT%\services\b" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY
robocopy "apps\ai-finance-hub\.next\standalone" "%OUT%\services\hub" /E >>"%LOG%" 2>&1
if errorlevel 8 goto FAILED_COPY
echo [4/7] Copying static and public assets...
for %%A in (life-ledger payment-simulator ai-finance-hub) do (
  if "%%A"=="life-ledger" set "DEST=a"
  if "%%A"=="payment-simulator" set "DEST=b"
  if "%%A"=="ai-finance-hub" set "DEST=hub"
  robocopy "apps\%%A\.next\static" "%OUT%\services\!DEST!\apps\%%A\.next\static" /E >>"%LOG%" 2>&1
  if errorlevel 8 goto FAILED_COPY
  if exist "apps\%%A\public" robocopy "apps\%%A\public" "%OUT%\services\!DEST!\apps\%%A\public" /E >>"%LOG%" 2>&1
  if errorlevel 8 goto FAILED_COPY
)
echo [5/7] Copying shared SQLite database and launchers...
copy /y "prisma\dev.db" "%OUT%\database\dev.db" >>"%LOG%" 2>&1 || goto FAILED_COPY
copy /y "scripts\portable-integrated-start.cmd" "%OUT%\START-PLATFORM.cmd" >nul
copy /y "scripts\portable-integrated-stop.cmd" "%OUT%\STOP-PLATFORM.cmd" >nul
copy /y "scripts\portable-integrated-run-a.cmd" "%OUT%\RUN-A.cmd" >nul
copy /y "scripts\portable-integrated-run-b.cmd" "%OUT%\RUN-B.cmd" >nul
copy /y "scripts\portable-integrated-run-hub.cmd" "%OUT%\RUN-HUB.cmd" >nul
(
 echo ACCOUNTING INTELLIGENT LEARNING AND TEACHING DECISION PLATFORM
 echo.
 echo 1. Extract the complete ZIP before running.
 echo 2. Double-click START-PLATFORM.cmd.
 echo 3. Keep the three server windows open.
 echo 4. Platform address: http://127.0.0.1:2999
 echo 5. Student: student_demo / demo1234
 echo 6. Teacher: teacher_demo / demo1234
 echo 7. This package uses local SQLite and Mock mode.
 echo 8. It contains no real API key and can run offline.
 echo 9. Stop by double-clicking STOP-PLATFORM.cmd.
 echo 10. Uninstall by stopping the platform and deleting this folder.
)>"%OUT%\README-FIRST.txt"
echo [6/7] Verifying package files...
for %%F in ("%OUT%\runtime\node.exe" "%OUT%\database\dev.db" "%OUT%\services\a\apps\life-ledger\server.js" "%OUT%\services\b\apps\payment-simulator\server.js" "%OUT%\services\hub\apps\ai-finance-hub\server.js") do if not exist %%F goto FAILED_COPY
echo [7/7] Creating ZIP. Please wait...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -LiteralPath '%OUT%' -DestinationPath '%ZIP%' -CompressionLevel Optimal -Force" >>"%LOG%" 2>&1
if errorlevel 1 goto FAILED_ZIP
echo SUCCESS: %ZIP%
>>"%LOG%" echo [%date% %time%] SUCCESS
start "" explorer.exe "%CD%\release"
goto END
:NO_NODE
set "ERR=Node.js was not found. Use Node.js 20 or 22 LTS."
goto SHOW
:NOT_READY
set "ERR=Dependencies or database missing. Run setup-first-time.cmd first."
goto SHOW
:FAILED_BUILD
set "ERR=Production build failed. See the log."
goto SHOW
:FAILED_STANDALONE
set "ERR=Standalone server output is missing."
goto SHOW
:FAILED_COPY
set "ERR=Failed to copy package files."
goto SHOW
:FAILED_ZIP
set "ERR=Failed to create ZIP."
:SHOW
echo ERROR: %ERR%
>>"%LOG%" echo ERROR: %ERR%
echo Log: %LOG%
pause
:END
endlocal
