@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM Common Ranking Updater Script
REM Usage: update_ranking_common.bat [github|image|video]
REM ============================================================

REM Parameter check
if "%~1"=="" (
    echo ERROR: Ranking type required
    echo Usage: update_ranking_common.bat [github^|image^|video]
    exit /b 255
)

set RANKING_TYPE=%~1

REM Validate ranking type
if /i not "%RANKING_TYPE%"=="github" (
    if /i not "%RANKING_TYPE%"=="image" (
        if /i not "%RANKING_TYPE%"=="video" (
            echo ERROR: Invalid ranking type: %RANKING_TYPE%
            echo Valid types: github, image, video
            exit /b 254
        )
    )
)

REM Set display name based on type
if /i "%RANKING_TYPE%"=="github" set DISPLAY_NAME=GitHub Trend Ranking
if /i "%RANKING_TYPE%"=="image" set DISPLAY_NAME=Image AI Ranking
if /i "%RANKING_TYPE%"=="video" set DISPLAY_NAME=Video AI Ranking

REM Configuration
set PROJECT_DIR=C:\Users\Tenormusica\ai-trend-daily
set PYTHON_EXE=C:\Users\Tenormusica\AppData\Local\Programs\Python\Python310\python.exe
set PYTHON_SCRIPT=update_%RANKING_TYPE%_ranking.py
set JSON_FILE=%RANKING_TYPE%_ranking.json
set GIT_REMOTE=origin
set GIT_BRANCH=main

REM Safe date/time format (avoid special characters)
set SAFE_DATE=%date:/=-%
set SAFE_TIME=%time::=-%
set SAFE_TIME=%SAFE_TIME: =0%

REM Locale-independent date for log file (fallback to %date% format)
for /f "tokens=*" %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd" 2^>nul') do set LOG_DATE=%%a
if not defined LOG_DATE set LOG_DATE=%date:~0,4%%date:~5,2%%date:~8,2%

REM Change to project directory with error check
cd /d "%PROJECT_DIR%"
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Failed to change directory to %PROJECT_DIR%
    exit /b 1
)

REM Create logs directory if not exists with error check
if not exist "logs" (
    mkdir logs
    if !ERRORLEVEL! NEQ 0 (
        echo ERROR: Failed to create logs directory
        exit /b 10
    )
)

REM Log file path
set LOG_FILE=logs\%RANKING_TYPE%_ranking_%LOG_DATE%.log

REM Test log file write access
echo [%time%] Log initialized for %DISPLAY_NAME% > "%LOG_FILE%" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Cannot write to log file %LOG_FILE%
    exit /b 11
)

REM Verify Python executable exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python executable not found: %PYTHON_EXE%
    echo [%time%] ERROR: Python not found >> "%LOG_FILE%"
    exit /b 12
)

REM Verify Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: Python script not found: %PYTHON_SCRIPT%
    echo [%time%] ERROR: Script file not found >> "%LOG_FILE%"
    exit /b 13
)

REM Verify git is available
where git >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: git not found in PATH
    echo [%time%] ERROR: git not found >> "%LOG_FILE%"
    exit /b 14
)

echo.
echo ============================================================
echo %DISPLAY_NAME% Daily Update
echo ============================================================
echo Started at: %date% %time%
echo.

REM Run Python script with full path
echo [%time%] Running Python script: %PYTHON_SCRIPT% >> "%LOG_FILE%"
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" >> "%LOG_FILE%" 2>&1
set PYTHON_RESULT=!ERRORLEVEL!

REM Check Python execution result
if !PYTHON_RESULT! NEQ 0 (
    echo.
    echo ============================================================
    echo ERROR: Python script failed with error code !PYTHON_RESULT!
    echo ============================================================
    echo [%time%] ERROR: Python script failed with code !PYTHON_RESULT! >> "%LOG_FILE%"
    set /a OFFSET_CODE=!PYTHON_RESULT!+100
    exit /b !OFFSET_CODE!
)

echo.
echo ============================================================
echo Python Script Completed Successfully!
echo ============================================================
echo [%time%] Python script completed successfully >> "%LOG_FILE%"

REM Validate output JSON file exists
if not exist "%JSON_FILE%" (
    echo ERROR: Output file not created: %JSON_FILE%
    echo [%time%] ERROR: %JSON_FILE% not found >> "%LOG_FILE%"
    exit /b 20
)

REM Validate JSON file size (minimum 100 bytes)
for %%A in ("%JSON_FILE%") do set FILE_SIZE=%%~zA
if !FILE_SIZE! LSS 100 (
    echo ERROR: Output file too small ^(!FILE_SIZE! bytes^) - possible data corruption
    echo [%time%] ERROR: File size check failed ^(!FILE_SIZE! bytes^) >> "%LOG_FILE%"
    exit /b 21
)

REM Validate JSON syntax
"%PYTHON_EXE%" -c "import json; json.load(open('%JSON_FILE%', encoding='utf-8'))" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: Invalid JSON format in %JSON_FILE%
    echo [%time%] ERROR: JSON validation failed >> "%LOG_FILE%"
    exit /b 22
)

echo [%time%] Output file validated: %JSON_FILE% ^(%FILE_SIZE% bytes^) >> "%LOG_FILE%"

REM Commit and push to GitHub with error handling
echo.
echo Committing changes to GitHub...

git add "%JSON_FILE%"
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: git add failed
    echo [%time%] ERROR: git add failed >> "%LOG_FILE%"
    exit /b 2
)

git commit -m "Auto-update %DISPLAY_NAME% - %SAFE_DATE% %SAFE_TIME%"
set COMMIT_RESULT=!ERRORLEVEL!
if !COMMIT_RESULT! NEQ 0 (
    if !COMMIT_RESULT! EQU 1 (
        echo No changes to commit - skipping push
        echo [%time%] No changes to commit >> "%LOG_FILE%"
        goto :finish
    ) else (
        echo ERROR: git commit failed with code !COMMIT_RESULT!
        echo [%time%] ERROR: git commit failed >> "%LOG_FILE%"
        exit /b 3
    )
)

REM Check for authentication errors before push
git push %GIT_REMOTE% %GIT_BRANCH% 2>&1 | findstr /i "Authentication denied fatal error" >nul
if !ERRORLEVEL! EQU 0 (
    echo ERROR: git push failed - Authentication error
    echo [%time%] ERROR: git push authentication failed >> "%LOG_FILE%"
    echo TIP: Check GITHUB_TOKEN environment variable or credential manager
    exit /b 4
)

git push %GIT_REMOTE% %GIT_BRANCH%
if !ERRORLEVEL! NEQ 0 (
    echo ERROR: git push failed
    echo [%time%] ERROR: git push failed >> "%LOG_FILE%"
    exit /b 4
)

echo.
echo Git push completed!
echo [%time%] Git push completed >> "%LOG_FILE%"

:finish
echo.
echo ============================================================
echo Daily Update Completed Successfully!
echo ============================================================

echo.
echo Finished at: %date% %time%
echo [%time%] Finished >> "%LOG_FILE%"
echo.

endlocal
exit /b 0
