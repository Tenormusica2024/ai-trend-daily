@echo off
REM 動画生成AIランキング自動更新タスク登録スクリプト（簡易版）

set TASK_NAME=AI_Video_Ranking_Daily_Update
set SCRIPT_PATH=%~dp0update_video_ranking.py

echo Setting up Video AI Ranking auto-update task...

REM 既存タスクを削除（エラーは無視）
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM 新しいタスクを作成（毎日午前3時実行）
schtasks /create /tn "%TASK_NAME%" /tr "python %SCRIPT_PATH%" /sc daily /st 03:00 /f

if %ERRORLEVEL% EQU 0 (
    echo OK Task registered successfully!
    echo Task Name: %TASK_NAME%
    echo Execution Time: Daily at 3:00 AM
    echo Script: %SCRIPT_PATH%
    echo.
    echo Manual test execution:
    echo   schtasks /run /tn "%TASK_NAME%"
) else (
    echo ERROR: Failed to register task
    exit /b 1
)
