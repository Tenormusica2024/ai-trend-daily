@echo off
REM GitHub Trend Ranking Daily Updater
REM Runs daily at 9:00 AM via Windows Task Scheduler
call "%~dp0update_ranking_common.bat" github
exit /b %ERRORLEVEL%
