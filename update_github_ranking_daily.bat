@echo off
REM GitHub Trend Ranking Daily Updater
REM Runs daily at 9:00 AM via Windows Task Scheduler

cd /d "C:\Users\Tenormusica\ai-trend-daily"

echo.
echo ============================================================
echo GitHub Trend Ranking Daily Update
echo ============================================================
echo Started at: %date% %time%
echo.

REM Run Python script
python update_github_ranking.py

REM Check if successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo Daily Update Completed Successfully!
    echo ============================================================
    
    REM Commit and push to GitHub
    echo.
    echo Committing changes to GitHub...
    git add github_ranking.json
    git commit -m "Auto-update GitHub Trend Ranking - %date% %time%"
    git push origin main
    
    echo.
    echo Git push completed!
) else (
    echo.
    echo ============================================================
    echo ERROR: Update failed with error code %ERRORLEVEL%
    echo ============================================================
)

echo.
echo Finished at: %date% %time%
echo.
