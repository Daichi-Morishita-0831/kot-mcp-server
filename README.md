# King of Time MCP Server

Claude Code から [King of Time](https://www.kingoftime.jp/) の勤怠管理を操作するための MCP サーバーです。

## できること

| カテゴリ | ツール | 説明 |
|---------|--------|------|
| 企業情報 | `get_company` | 企業情報取得 |
| 企業情報 | `list_administrators` | 管理者一覧 |
| 従業員 | `list_employees` | 従業員一覧（所属フィルタ可） |
| 従業員 | `get_employee` | 従業員詳細 |
| 従業員 | `list_divisions` | 所属（部署）一覧 |
| 従業員 | `list_working_types` | 雇用区分一覧 |
| 従業員 | `list_employee_groups` | 従業員グループ一覧 |
| 勤怠 | `get_daily_workings` | 日別勤怠データ |
| 勤怠 | `get_monthly_workings` | 月別勤怠集計 |
| 勤怠 | `get_yearly_holidays` | 年別休暇データ |
| 打刻 | `record_time` | 出勤/退勤/外出/戻り打刻 |
| 申請管理 | `get_schedule_requests` | スケジュール申請一覧 |
| 申請管理 | `approve_request` | 申請承認 |
| 申請管理 | `reject_request` | 申請棄却 |
| 設定 | `check_token` | APIトークン有効確認 |

## セットアップ

### 1. API アクセストークンを取得

1. King of Time 管理画面にログイン
2. **設定** → **その他** → **オプション** を開く
3. **外部サービス連携** → **KING OF TIME WebAPI連携設定** を選択
4. アクセストークンを発行（またはコピー）

### 2. インストール

```bash
# uv がない場合は先にインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクトの依存関係をインストール
cd kot-mcp-server
uv sync
```

### 3. Claude Code に登録

`~/.claude/settings.json` の `mcpServers` に追加:

```json
{
  "mcpServers": {
    "king-of-time": {
      "command": "uv",
      "args": ["--directory", "/Users/あなたのユーザー名/kot-mcp-server", "run", "kot-mcp-server"],
      "env": {
        "KOT_ACCESS_TOKEN": "ここにトークンを貼り付け"
      }
    }
  }
}
```

### 4. Claude Code を再起動

Claude Code を再起動すると、King of Time のツールが使えるようになります。

## 使い方の例

Claude Code で以下のように話しかけるだけ:

- 「今月の勤怠データを見せて」
- 「田中さんの今日の勤怠を確認して」
- 「未承認の申請を一覧表示して」
- 「申請ID xxx を承認して」
- 「営業部の従業員一覧を出して」

## トラブルシューティング

### `KOT_ACCESS_TOKEN が未設定です` エラー
→ `settings.json` の `env` にトークンが正しくセットされているか確認

### `429 Rate limited` エラー
→ API のレートリミット。自動リトライしますが、短時間に大量リクエストは避けてください

### トークンが無効
→ `check_token` ツールで確認。期限切れの場合は King of Time 管理画面で再発行
