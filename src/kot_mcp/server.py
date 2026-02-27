"""King of Time MCP Server.

Claude Code から King of Time の勤怠管理を操作するための MCP サーバー。
従業員管理、勤怠データ取得、打刻、申請承認/棄却をサポート。
"""

from __future__ import annotations

import json
import os

from mcp.server.fastmcp import FastMCP

from kot_mcp.client import KingOfTimeClient, KotApiError

mcp = FastMCP(
    "King of Time",
    instructions=(
        "King of Time 勤怠管理システムの MCP サーバーです。"
        "従業員管理、勤怠データ取得、打刻登録、申請の承認・棄却ができます。"
        "日付は YYYY-MM-DD 形式、年月は YYYY-MM 形式で指定してください。"
    ),
)


def _get_client() -> KingOfTimeClient:
    """環境変数からトークンを読み込み、クライアントを生成."""
    token = os.environ.get("KOT_ACCESS_TOKEN", "")
    if not token:
        raise RuntimeError(
            "KOT_ACCESS_TOKEN が未設定です。"
            "King of Time 管理画面 → 設定 → 外部サービス連携 → WebAPI で取得してください。"
        )
    return KingOfTimeClient(token)


def _fmt(data: object) -> str:
    """API レスポンスを整形して返す."""
    return json.dumps(data, ensure_ascii=False, indent=2)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  企業・管理者
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def get_company() -> str:
    """企業情報を取得します。企業コード・企業名などの基本情報を返します。"""
    client = _get_client()
    try:
        result = await client.get_company()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def list_administrators() -> str:
    """管理者一覧を取得します。管理者の名前・メールアドレス・所属情報を返します。"""
    client = _get_client()
    try:
        result = await client.list_administrators()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  従業員管理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def list_employees(division_code: str | None = None) -> str:
    """従業員一覧を取得します。

    Args:
        division_code: 所属コードでフィルタ（省略時は全員）
    """
    client = _get_client()
    try:
        result = await client.list_employees(division_code=division_code)
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def get_employee(employee_code: str) -> str:
    """従業員の詳細情報を取得します。

    Args:
        employee_code: 従業員コード
    """
    client = _get_client()
    try:
        result = await client.get_employee(employee_code)
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def list_divisions() -> str:
    """所属（部署）一覧を取得します。"""
    client = _get_client()
    try:
        result = await client.list_divisions()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def list_working_types() -> str:
    """雇用区分一覧を取得します。"""
    client = _get_client()
    try:
        result = await client.list_working_types()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def list_employee_groups() -> str:
    """従業員グループ一覧を取得します。"""
    client = _get_client()
    try:
        result = await client.list_employee_groups()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  勤怠データ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def get_daily_workings(
    date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    division_code: str | None = None,
) -> str:
    """日別の勤怠データを取得します。

    Args:
        date: 特定日の勤怠を取得 (YYYY-MM-DD)
        start_date: 期間指定の開始日 (YYYY-MM-DD)
        end_date: 期間指定の終了日 (YYYY-MM-DD)
        division_code: 所属コードでフィルタ
    """
    client = _get_client()
    try:
        result = await client.get_daily_workings(
            date=date,
            start_date=start_date,
            end_date=end_date,
            division_code=division_code,
        )
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def get_monthly_workings(
    date: str,
    division_code: str | None = None,
) -> str:
    """月別の勤怠集計データを取得します。

    Args:
        date: 対象年月 (YYYY-MM)
        division_code: 所属コードでフィルタ
    """
    client = _get_client()
    try:
        result = await client.get_monthly_workings(
            date=date, division_code=division_code
        )
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def get_yearly_holidays(type_code: str, year: int) -> str:
    """年別の休暇データを取得します。

    Args:
        type_code: 休暇種別コード
        year: 対象年 (例: 2026)
    """
    client = _get_client()
    try:
        result = await client.get_yearly_holidays(type_code=type_code, year=year)
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  打刻
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def record_time(
    employee_key: str,
    record_type: int,
    date: str | None = None,
    time: str | None = None,
) -> str:
    """打刻を登録します。出勤・退勤・外出・戻りの記録ができます。

    Args:
        employee_key: 従業員キー
        record_type: 打刻種別 (1:出勤, 2:退勤, 3:外出, 4:戻り)
        date: 打刻日 (YYYY-MM-DD)。省略時は当日
        time: 打刻時刻 (HH:MM)。省略時は現在時刻
    """
    client = _get_client()
    try:
        result = await client.record_time(
            employee_key=employee_key,
            record_type=record_type,
            date=date,
            time=time,
        )
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  申請管理（管理職向け）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def get_schedule_requests(date: str) -> str:
    """指定日のスケジュール申請一覧を取得します。管理職向け。

    Args:
        date: 対象日 (YYYY-MM-DD)
    """
    client = _get_client()
    try:
        result = await client.get_schedule_requests(date=date)
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def approve_request(request_id: str) -> str:
    """申請を承認します。管理職向け。

    Args:
        request_id: 承認する申請のID
    """
    client = _get_client()
    try:
        result = await client.approve_request(request_id)
        return _fmt(result) if result else "承認しました"
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


@mcp.tool()
async def reject_request(request_id: str, reason: str = "") -> str:
    """申請を棄却します。管理職向け。

    Args:
        request_id: 棄却する申請のID
        reason: 棄却理由（任意）
    """
    client = _get_client()
    try:
        result = await client.reject_request(request_id, reason=reason)
        return _fmt(result) if result else "棄却しました"
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  トークン確認
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool()
async def check_token() -> str:
    """API トークンが有効かどうか確認します。接続テストに使えます。"""
    client = _get_client()
    try:
        result = await client.check_token()
        return _fmt(result)
    except KotApiError as e:
        return f"エラー: {e}"
    finally:
        await client.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  エントリポイント
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main() -> None:
    """MCP サーバーを stdio トランスポートで起動."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
