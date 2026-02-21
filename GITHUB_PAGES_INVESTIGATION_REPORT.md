# GitHub Pages プログラム有効化調査結果

調査日時: 2025-10-24

## 調査完了（2024年最新情報）

**結論: GitHub Actionsによるプログラム的な初回有効化は不可能**

---

## API制限の詳細

### 1. GitHub REST API の制約（2024年セキュリティ強化）

- **GitHub Apps からの Pages 有効化は完全禁止**（セキュリティ上の理由）
- **Personal Access Token（repo権限）が必須**
- トークン認証なしではAPI経由の有効化は不可能

**参考資料:**
- [GitHub Community Discussion #35595](https://github.com/orgs/community/discussions/35595)
- [GitHub Pages REST API Documentation](https://docs.github.com/en/rest/pages/pages)

### 2. GitHub Actions デプロイの前提条件

- GitHub Actions ワークフローを使用するには**初回のPages有効化が必須**
- 初回のみユーザーがGitHub Web UIで有効化する必要がある
- 有効化後はワークフローが自動実行される

### 3. cloud-market-racing-chart（昨日成功）との違い

| プロジェクト | デプロイ方式 | 初回設定 |
|-------------|-------------|---------|
| cloud-market-racing-chart | Deploy from branch | 不要 |
| ai-trend-daily | GitHub Actions | **必須** |

**なぜ昨日はできて今日はできないのか？**

- 昨日の cloud-market-racing-chart は "Deploy from branch" 方式を使用
- この方式は GitHub が自動的にファイルを検出してデプロイ
- 今回試行した "GitHub Actions" 方式は初回の手動有効化が必須

---

## 推奨解決策: Deploy from branch 方式

既に **root直下にファイル配置完済**（commit cfb3b6e）

### ✅ 必要な操作（1分で完了）

1. **GitHub リポジトリ設定を開く:**
   ```
   https://github.com/Tenormusica2024/ai-trend-daily/settings/pages
   ```

2. **以下を設定:**
   - **Source**: Deploy from a branch
   - **Branch**: main
   - **フォルダ**: / (root)
   - **Save** をクリック

3. **1-2分待機**

4. **アクセス確認:**
   ```
   https://tenormusica2024.github.io/ai-trend-daily/
   ```

---

## Deploy from branch 方式のメリット

- ✅ **シンプル**（設定1回のみ）
- ✅ **自動更新**（main ブランチへの push で自動デプロイ）
- ✅ **トークン・認証不要**
- ✅ **cloud-market-racing-chart と同じ方式**

---

## 技術的補足

### API エンドポイント（トークン必須）

```bash
POST /repos/{owner}/{repo}/pages
```

**必要な権限:**
- Repository administrator
- Maintainer
- 'manage GitHub Pages settings' permission
- Personal Access Token (classic) with `repo` scope

### GitHub Actions ワークフロー（既に作成済み）

- ファイル: `.github/workflows/pages.yml`
- 用途: 将来の自動更新用（初回有効化後に動作）

---

## ファイル準備完了 ✅

- ✅ `index.html`（root）
- ✅ `surge_ranking.json`（root）
- ✅ `.github/workflows/pages.yml`（将来の自動更新用）
- ✅ `docs/index.html`（バックアップ）
- ✅ `docs/surge_ranking.json`（バックアップ）

---

## 参考資料

1. **GitHub REST API Documentation**
   - https://docs.github.com/en/rest/pages/pages

2. **GitHub Community Discussion #35595**
   - https://github.com/orgs/community/discussions/35595
   - "Can't enable a Github Pages site from the API anymore"

3. **Automated Application Deployment**
   - https://resources.github.com/learn/pathways/automation/essentials/automated-application-deployment-with-github-actions-and-pages/

4. **Stack Overflow Discussion**
   - https://stackoverflow.com/questions/48620366/programmatically-enable-github-pages-for-a-repository

---

## 結論

**プログラム的な初回有効化は2024年のセキュリティ強化により不可能。**

**推奨アクション:**
- GitHub Web UI で "Deploy from branch" を設定（1分）
- 以降は自動デプロイが機能

設定完了後、即座に https://tenormusica2024.github.io/ai-trend-daily/ でアクセス可能になります。
