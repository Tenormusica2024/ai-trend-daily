# AI Trend Daily - Windows Task Scheduler Setup (PowerShell)
# 3時間ごと: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00

$TaskName = "AITrendDaily3Hour"
$PythonPath = "C:\Users\Tenormusica\AppData\Local\Programs\Python\Python310\python.exe"
$ScriptPath = "C:\Users\Tenormusica\ai-trend-daily\auto_update.py"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "AI Trend Daily - Task Scheduler Setup (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 既存タスク削除
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[INFO] Deleting existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# アクション定義（Python実行）
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath

# トリガー定義（8つの時刻: 3時間ごと）
$Triggers = @()
$Times = @("00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00")

foreach ($Time in $Times) {
    $Trigger = New-ScheduledTaskTrigger -Daily -At $Time
    $Triggers += $Trigger
}

# 設定
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# タスク登録
Write-Host "[INFO] Creating task with 8 triggers (3-hour intervals)..." -ForegroundColor Green
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Triggers -Settings $Settings -RunLevel Highest -Force | Out-Null

if ($?) {
    Write-Host "[OK] Task created successfully: $TaskName" -ForegroundColor Green
    Write-Host ""
    Write-Host "Execution Schedule:" -ForegroundColor Cyan
    foreach ($Time in $Times) {
        Write-Host "  - $Time" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "Setup Completed Successfully" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Verify with: Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo" -ForegroundColor Yellow
    Write-Host "Test manually: Start-ScheduledTask -TaskName $TaskName" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Failed to create task" -ForegroundColor Red
    exit 1
}
