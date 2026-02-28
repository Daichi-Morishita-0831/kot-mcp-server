# King of Time MCP Server

King of Time (キングオブタイム) REST API をラップした MCP サーバー。
従業員の勤怠管理・打刻・申請承認を Claude Code から直接操作できる。

## ツール一覧

### 情報取得系（読み取り専用・安全）

| ツール名 | 用途 | 主な引数 |
|---------|------|---------|
| `check_token` | API 接続テスト | なし |
| `get_company` | 会社情報の取得 | なし |
| `list_administrators` | 管理者一覧 | なし |
| `list_employees` | 全従業員の一覧 | `division_code?` |
| `get_employee` | 従業員の詳細情報 | `employee_code` |
| `list_divisions` | 部署一覧 | なし |
| `list_working_types` | 勤務パターン一覧 | なし |
| `list_employee_groups` | 従業員グループ一覧 | なし |
| `get_daily_workings` | 日次勤怠データ | `date`, `employee_code?` |
| `get_monthly_workings` | 月次勤怠データ | `year_month` (YYYY-MM), `employee_code?` |
| `get_yearly_holidays` | 年次有給休暇データ | `year` (YYYY), `employee_code?` |

### スケジュール申請系

| ツール名 | 用途 | 主な引数 |
|---------|------|---------|
| `get_schedule_requests` | スケジュール申請一覧 | `status?` (applying/approved/rejected) |

### 書き込み系（⚠️ データ変更あり）

| ツール名 | 用途 | 主な引数 |
|---------|------|---------|
| `record_time` | 打刻の記録 | `employee_code`, `date`, `time`, `record_type` (clock_in/clock_out) |
| `approve_request` | 申請の承認 | `request_id` |
| `reject_request` | 申請の却下 | `request_id`, `reason?` |

## よくある使い方（プロンプト例）

### 日常チェック
```
今日の全従業員の勤怠状況を教えて
```
```
今月の残業時間が多い従業員を教えて
```
```
有給休暇の残日数が少ない従業員は？
```

### 承認業務
```
未承認のスケジュール申請を一覧表示して
```
```
申請ID xxx を承認して
```

### 打刻修正
```
従業員コード 001 の 2026-02-28 の出勤打刻を 09:00 に修正して
```

## 注意事項

- **書き込み系ツール**（record_time, approve_request, reject_request）は実データを変更するため、実行前に必ず確認する
- `date` 形式: `YYYY-MM-DD`
- `year_month` 形式: `YYYY-MM`
- `time` 形式: `HH:MM`
- API レート制限あり（429 発生時は自動リトライする）
- 部署コードでフィルタ可能なツールは `division_code` 引数を指定

## 技術情報

- ランタイム: Python 3.14+（uv 管理）
- フレームワーク: FastMCP (mcp[cli])
- HTTP クライアント: httpx（非同期）
- API ベース URL: `https://api.kingtime.jp/v1.0`
- 認証: Bearer トークン（環境変数 `KOT_ACCESS_TOKEN`）
- トランスポート: stdio

## 開発コマンド

```bash
# 依存インストール
uv sync

# サーバー起動テスト
uv run kot-mcp-server

# ツール一覧確認
uv run python -c "from kot_mcp.server import mcp; print([t.name for t in mcp._tool_manager.list_tools()])"
```
