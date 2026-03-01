# Windows Task Scheduler 設定マニュアル

## 自動実行（管理者権限不要の方法）

### オプション1: Windows起動時スクリプト（推奨）

**フォルダパス:**
```
C:\Users\Tenormusica\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

**手順:**
1. 以下の内容で `ai_trend_auto_start.vbs` を作成:

```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "python C:\Users\Tenormusica\ai-trend-daily\auto_update.py", 0, False
WScript.Sleep 10800000 ' 3時間 = 10,800,000ミリ秒
```

2. このファイルをスタートアップフォルダに配置
3. PC起動時に自動実行され、3時間ごとにループ実行

---

### オプション2: PowerShell（管理者権限で実行）

**⚠️ 管理者権限のPowerShellで実行してください:**

```powershell
# 管理者権限でPowerShellを開く
# 方法: スタートメニュー > PowerShell を右クリック > 管理者として実行

cd C:\Users\Tenormusica\ai-trend-daily
.\create_task_simple.ps1
```

**確認コマンド:**
```powershell
Get-ScheduledTask -TaskName AITrendDaily3Hour | Select-Object -ExpandProperty Triggers
```

**テスト実行:**
```powershell
Start-ScheduledTask -TaskName AITrendDaily3Hour
```

---

### オプション3: 手動でTask Schedulerから設定

1. **タスクスケジューラを開く:**
   - Windowsキー → "タスク スケジューラ" と検索

2. **新規タスク作成:**
   - "操作" メニュー → "基本タスクの作成"

3. **設定内容:**
   - **名前**: `AITrendDaily3Hour`
   - **トリガー**: 毎日
   - **開始時刻**: 00:00
   - **操作**: プログラムの開始
     - プログラム: `C:\Users\Tenormusica\AppData\Local\Programs\Python\Python310\python.exe`
     - 引数: `C:\Users\Tenormusica\ai-trend-daily\auto_update.py`

4. **追加トリガー作成（3時間ごと）:**
   - タスクを右クリック → "プロパティ"
   - "トリガー" タブ → "新規" をクリック
   - 以下の時刻で7つのトリガーを追加:
     - 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00

---

## 実行確認

### 手動テスト実行:
```bash
cd C:\Users\Tenormusica\ai-trend-daily
python auto_update.py
```

### 出力ファイル確認:
- **JSON**: `C:\Users\Tenormusica\ai-trend-daily\output\ranking.json`
- **HTML**: `C:\Users\Tenormusica\ai-trend-daily\output\ranking.html`
- **データベース**: `C:\Users\Tenormusica\ai-trend-daily\data\trends.db`

### ログ確認:
```bash
cat ai-trend-daily/update_log.txt
```

---

## トラブルシューティング

### 1. "Access is denied" エラー
- PowerShellを**管理者権限で実行**してください
- または**オプション1（Startup）**を使用（管理者権限不要）

### 2. タスクが実行されない
```powershell
# タスクの状態確認
Get-ScheduledTask -TaskName AITrendDaily3Hour | Get-ScheduledTaskInfo

# 最終実行時刻・次回実行時刻を確認
```

### 3. Pythonパスが異なる場合
```bash
# Pythonパス確認
where python
```

上記コマンドで表示されたパスをスクリプト内の `PythonPath` に設定

---

## 実行スケジュール

**1日8回実行（3時間間隔）:**
- 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00

**データ保持期間:**
- 7日間（自動クリーンアップ）

**API制限:**
- Wikipedia Pageviews API: 200ms間隔
- タイムアウト: 60秒
