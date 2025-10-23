@echo off
REM AI Trend Daily - Windows Task Scheduler 3時間間隔設定
REM 実行時刻: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00

echo ======================================================================
echo AI Trend Daily - Task Scheduler Setup
echo ======================================================================
echo.

REM タスク名
set TASK_NAME=AITrendDaily3Hour

REM プロジェクトディレクトリ
set PROJECT_DIR=C:\Users\Tenormusica\ai-trend-daily

REM Pythonパス（自動検出）
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i

echo Task Name: %TASK_NAME%
echo Project Directory: %PROJECT_DIR%
echo Python Path: %PYTHON_PATH%
echo Script: %PROJECT_DIR%\auto_update.py
echo.

REM 既存タスク削除（存在する場合）
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Deleting existing task...
    schtasks /delete /tn "%TASK_NAME%" /f
)

echo [INFO] Creating new task with 3-hour intervals...
echo.

REM タスク作成（3時間ごと = 1日8回実行）
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\auto_update.py\"" ^
    /sc daily ^
    /mo 1 ^
    /st 00:00 ^
    /rl highest ^
    /f

if %ERRORLEVEL% EQU 0 (
    echo [OK] Task created: %TASK_NAME%
    echo.
    echo Execution Schedule:
    echo - 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00
    echo.
    
    REM 3時間間隔の追加トリガー作成（XML編集が必要）
    echo [INFO] Adding additional triggers for 3-hour intervals...
    
    REM タスクXMLをエクスポート
    schtasks /query /tn "%TASK_NAME%" /xml > "%TEMP%\%TASK_NAME%.xml"
    
    REM PowerShellでXML編集して3時間間隔のトリガー追加
    powershell -ExecutionPolicy Bypass -Command ^
        "$xml = [xml](Get-Content '%TEMP%\%TASK_NAME%.xml'); ^
        $triggers = $xml.Task.Triggers; ^
        $baseTrigger = $triggers.CalendarTrigger[0]; ^
        $times = @('03:00:00', '06:00:00', '09:00:00', '12:00:00', '15:00:00', '18:00:00', '21:00:00'); ^
        foreach ($time in $times) { ^
            $newTrigger = $baseTrigger.CloneNode($true); ^
            $newTrigger.StartBoundary = $newTrigger.StartBoundary -replace 'T\d{2}:\d{2}:\d{2}', ('T' + $time); ^
            [void]$triggers.AppendChild($newTrigger); ^
        }; ^
        $xml.Save('%TEMP%\%TASK_NAME%_modified.xml')"
    
    REM 修正したXMLで再作成
    schtasks /create /tn "%TASK_NAME%" /xml "%TEMP%\%TASK_NAME%_modified.xml" /f
    
    REM 一時ファイル削除
    del "%TEMP%\%TASK_NAME%.xml" >nul 2>&1
    del "%TEMP%\%TASK_NAME%_modified.xml" >nul 2>&1
    
    echo.
    echo ======================================================================
    echo Setup Completed Successfully
    echo ======================================================================
    echo.
    echo You can verify the task with:
    echo   schtasks /query /tn "%TASK_NAME%" /fo list /v
    echo.
    echo To test manually:
    echo   schtasks /run /tn "%TASK_NAME%"
    echo.
) else (
    echo [ERROR] Failed to create task
    pause
    exit /b 1
)

pause
