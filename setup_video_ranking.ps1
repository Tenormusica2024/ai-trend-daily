# 動画生成AIランキング自動更新タスク作成スクリプト
# Windows Task Schedulerに毎日定時実行タスクを登録

$TaskName = "AI_Video_Ranking_Daily_Update"
$ScriptPath = Join-Path $PSScriptRoot "update_video_ranking.py"
$PythonPath = "python"

# タスクが既に存在する場合は削除
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# タスクアクション: Pythonスクリプト実行
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory $PSScriptRoot

# トリガー: 毎日午前3時に実行
$Trigger = New-ScheduledTaskTrigger -Daily -At "3:00AM"

# タスク設定
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# タスク登録
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Video AI Ranking daily auto-update (runs at 3AM)"

Write-Host "OK Task Scheduler registration completed!"
Write-Host "Task Name: $TaskName"
Write-Host "Execution Time: Daily at 3:00 AM"
Write-Host "Script: $ScriptPath"
Write-Host ""
Write-Host "Manual test execution:"
Write-Host "  Start-ScheduledTask -TaskName AI_Video_Ranking_Daily_Update"
