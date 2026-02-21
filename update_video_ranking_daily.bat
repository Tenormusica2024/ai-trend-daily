@echo off
REM Video AI Ranking Daily Updater
REM Runs daily at 3:00 AM via Windows Task Scheduler
call "%~dp0update_ranking_common.bat" video
exit /b %ERRORLEVEL%
