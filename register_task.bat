@echo off
schtasks /create /tn "GitHub_Trend_Ranking_Daily_Update" /tr "cmd.exe /c C:\Users\Tenormusica\ai-trend-daily\update_github_ranking_daily.bat" /sc daily /st 09:00 /f
pause
