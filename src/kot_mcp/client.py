"""King of Time REST API クライアント."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.kingtime.jp/v1.0"


class KotApiError(Exception):
    """King of Time API エラー."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")


class KingOfTimeClient:
    """King of Time API の非同期クライアント.

    全エンドポイントをカバーし、429 レートリミット時は自動リトライする。
    """

    def __init__(self, access_token: str) -> None:
        self._token = access_token
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    # ── HTTP ヘルパー ──────────────────────────────────

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        max_retries: int = 3,
    ) -> Any:
        """HTTP リクエストを送信。429 は指数バックオフでリトライ。"""
        for attempt in range(max_retries):
            resp = await self._client.request(
                method, path, params=params, json=json_body
            )

            if resp.status_code == 429:
                wait = 2 ** attempt
                logger.warning("Rate limited (429). Retry in %ds...", wait)
                await asyncio.sleep(wait)
                continue

            if resp.status_code >= 400:
                body = resp.text
                raise KotApiError(resp.status_code, body)

            if resp.status_code == 204:
                return None

            return resp.json()

        raise KotApiError(429, "Rate limit exceeded after retries")

    async def _get(self, path: str, **params: Any) -> Any:
        filtered = {k: v for k, v in params.items() if v is not None}
        return await self._request("GET", path, params=filtered or None)

    async def _post(self, path: str, body: dict[str, Any]) -> Any:
        return await self._request("POST", path, json_body=body)

    async def _put(self, path: str, body: dict[str, Any]) -> Any:
        return await self._request("PUT", path, json_body=body)

    async def _delete(self, path: str) -> Any:
        return await self._request("DELETE", path)

    # ── 企業・管理者 ───────────────────────────────────

    async def get_company(self) -> dict:
        """企業情報を取得."""
        return await self._get("/company")

    async def list_administrators(self) -> list[dict]:
        """管理者一覧を取得."""
        return await self._get("/administrators")

    # ── 従業員管理 ─────────────────────────────────────

    async def list_employees(
        self,
        division_code: str | None = None,
    ) -> list[dict]:
        """従業員一覧を取得."""
        return await self._get(
            "/employees",
            divisionCode=division_code,
        )

    async def get_employee(self, employee_code: str) -> dict:
        """従業員詳細を取得."""
        return await self._get(f"/employees/{employee_code}")

    async def list_divisions(self) -> list[dict]:
        """所属（部署）一覧を取得."""
        return await self._get("/divisions")

    async def list_working_types(self) -> list[dict]:
        """雇用区分一覧を取得."""
        return await self._get("/working-types")

    async def list_employee_groups(self) -> list[dict]:
        """従業員グループ一覧を取得."""
        return await self._get("/employee-groups")

    # ── 勤怠データ ─────────────────────────────────────

    async def get_daily_workings(
        self,
        date: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        division_code: str | None = None,
    ) -> list[dict]:
        """日別勤怠データを取得.

        Args:
            date: 特定日 (YYYY-MM-DD)
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            division_code: 所属コードでフィルタ
        """
        return await self._get(
            "/daily-workings",
            date=date,
            startDate=start_date,
            endDate=end_date,
            divisionCode=division_code,
        )

    async def get_monthly_workings(
        self,
        date: str,
        division_code: str | None = None,
    ) -> list[dict]:
        """月別勤怠データを取得.

        Args:
            date: 対象年月 (YYYY-MM)
            division_code: 所属コードでフィルタ
        """
        return await self._get(
            f"/monthly-workings/{date}",
            divisionCode=division_code,
        )

    async def get_yearly_holidays(
        self,
        type_code: str,
        year: int,
    ) -> list[dict]:
        """年別休暇データを取得.

        Args:
            type_code: 休暇種別コード
            year: 対象年
        """
        return await self._get(
            f"/yearly-workings/holidays/{type_code}/{year}"
        )

    # ── 打刻 ───────────────────────────────────────────

    async def record_time(
        self,
        employee_key: str,
        record_type: int,
        date: str | None = None,
        time: str | None = None,
    ) -> dict:
        """打刻を登録.

        Args:
            employee_key: 従業員キー
            record_type: 打刻種別 (1:出勤, 2:退勤, 3:外出, 4:戻り)
            date: 打刻日 (YYYY-MM-DD)。省略時は当日
            time: 打刻時刻 (HH:MM)。省略時は現在時刻
        """
        body: dict[str, Any] = {"type": record_type}
        if date:
            body["date"] = date
        if time:
            body["time"] = time
        return await self._post(
            f"/daily-workings/timerecord/{employee_key}",
            body,
        )

    # ── 申請管理（管理職向け） ─────────────────────────

    async def get_schedule_requests(
        self,
        date: str,
    ) -> list[dict]:
        """スケジュール申請一覧を取得.

        Args:
            date: 対象日 (YYYY-MM-DD)
        """
        return await self._get(f"/schedule-requests/{date}")

    async def approve_request(self, request_id: str) -> dict:
        """申請を承認.

        Args:
            request_id: 申請ID
        """
        return await self._put(
            f"/requests/{request_id}",
            {"action": "approve"},
        )

    async def reject_request(
        self,
        request_id: str,
        reason: str = "",
    ) -> dict:
        """申請を棄却.

        Args:
            request_id: 申請ID
            reason: 棄却理由
        """
        body: dict[str, Any] = {"action": "reject"}
        if reason:
            body["reason"] = reason
        return await self._put(f"/requests/{request_id}", body)

    # ── トークン管理 ───────────────────────────────────

    async def check_token(self) -> dict:
        """トークンの有効性を確認."""
        return await self._get(f"/tokens/{self._token}/available")
