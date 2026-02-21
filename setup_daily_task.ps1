# GitHub Trend Ranking Daily Task Setup
# Creates a scheduled task to run update_github_ranking_daily.bat every day at 9:00 AM

$TaskName = "GitHub_Trend_Ranking_Daily_Update"
$Description = "Updates GitHub Trend Ranking data daily at 9:00 AM"
$ScriptPath = "C:\Users\Tenormusica\ai-trend-daily\update_github_ranking_daily.bat"
$TriggerTime = "09:00"

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "Task '$TaskName' already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create trigger (daily at 9:00 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Create principal (run with highest privileges)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $Description `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Force

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Task '$TaskName' has been created successfully!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Schedule: Daily at $TriggerTime" -ForegroundColor Cyan
Write-Host "Script: $ScriptPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify the task, run:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run the task manually, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
Write-Host ""
