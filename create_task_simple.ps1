# AI Trend Daily - Simple Task Scheduler Setup
# Creates single task at 00:00, then manually adds 7 more triggers

$TaskName = "AITrendDaily3Hour"
$PythonPath = "C:\Users\Tenormusica\AppData\Local\Programs\Python\Python310\python.exe"
$ScriptPath = "C:\Users\Tenormusica\ai-trend-daily\auto_update.py"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "AI Trend Daily - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 既存タスク削除
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[INFO] Deleting existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# ステップ1: 最初のトリガー（00:00）でタスク作成
Write-Host "[INFO] Creating base task (00:00 trigger)..." -ForegroundColor Green
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath
$Trigger = New-ScheduledTaskTrigger -Daily -At "00:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -RunLevel Highest -Force | Out-Null

if (!$?) {
    Write-Host "[ERROR] Failed to create base task" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Base task created" -ForegroundColor Green

# ステップ2: 追加トリガー（3時間ごと）をXML経由で追加
Write-Host "[INFO] Adding additional triggers (03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)..." -ForegroundColor Green

$Task = Get-ScheduledTask -TaskName $TaskName
$AdditionalTimes = @("03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00")

foreach ($Time in $AdditionalTimes) {
    $NewTrigger = New-ScheduledTaskTrigger -Daily -At $Time
    $Task.Triggers += $NewTrigger
}

$Task | Set-ScheduledTask -User $env:USERNAME | Out-Null

Write-Host "[OK] All 8 triggers added successfully" -ForegroundColor Green
Write-Host ""
Write-Host "Execution Schedule:" -ForegroundColor Cyan
Write-Host "  - 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00" -ForegroundColor White
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Setup Completed Successfully" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verify: Get-ScheduledTask -TaskName $TaskName | Select-Object -ExpandProperty Triggers" -ForegroundColor Yellow
Write-Host "Test: Start-ScheduledTask -TaskName $TaskName" -ForegroundColor Yellow
