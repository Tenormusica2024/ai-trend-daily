# 動画生成AIランキング自動更新タスク作成スクリプト
# Windows Task Schedulerに毎日定時実行タスクを登録

$TaskName = "AI_Video_Ranking_Daily_Update"
$ScriptPath = "$PSScriptRoot\update_video_ranking.py"
$PythonPath = "python"

# タスクが既に存在する場合は削除
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Write-Host "既存のタスクを削除します..."
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
    -Description "動画生成AIランキングを毎日自動更新（午前3時実行）"

Write-Host "✅ タスクスケジューラに登録完了！"
Write-Host "タスク名: $TaskName"
Write-Host "実行時刻: 毎日午前3時"
Write-Host "スクリプト: $ScriptPath"
Write-Host ""
Write-Host "手動実行テスト:"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
