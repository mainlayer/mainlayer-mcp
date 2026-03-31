"""
Mainlayer API client — thin async wrapper around the Mainlayer REST API.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_URL = "https://api.mainlayer.fr"


class MainlayerError(Exception):
    """Raised when the Mainlayer API returns an error response."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class MainlayerClient:
    """Synchronous HTTP client for the Mainlayer API."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        data = json.dumps(body).encode() if body is not None else None
        req = Request(url, data=data, headers=headers, method=method)

        try:
            with urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as exc:
            error_message = f"HTTP {exc.code}: {exc.reason}"
            try:
                error_body = json.loads(exc.read().decode())
                error_message = error_body.get("error") or error_body.get("message") or error_message
            except Exception:
                pass
            raise MainlayerError(error_message, status=exc.code) from exc

    # ------------------------------------------------------------------
    # Buyer tools
    # ------------------------------------------------------------------

    def discover_resources(
        self,
        *,
        query: str | None = None,
        type: str | None = None,
        fee_model: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if type:
            params["type"] = type
        if fee_model:
            params["fee_model"] = fee_model
        if limit is not None:
            params["limit"] = str(limit)
        qs = f"?{urlencode(params)}" if params else ""
        return self._request("GET", f"/discover{qs}")

    def get_resource_info(self, resource_id: str) -> dict[str, Any]:
        return self._request("GET", f"/resources/public/{resource_id}")

    def pay_for_resource(
        self,
        *,
        resource_id: str,
        payer_wallet: str,
        coupon_code: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "resource_id": resource_id,
            "payer_wallet": payer_wallet,
        }
        if coupon_code is not None:
            body["coupon_code"] = coupon_code
        return self._request("POST", "/pay", body)

    def check_access(
        self,
        *,
        resource_id: str,
        payer_wallet: str,
    ) -> dict[str, Any]:
        qs = urlencode({"resource_id": resource_id, "payer_wallet": payer_wallet})
        return self._request("GET", f"/entitlements/check?{qs}")

    # ------------------------------------------------------------------
    # Vendor tools
    # ------------------------------------------------------------------

    def create_resource(
        self,
        *,
        slug: str,
        type: str,
        price_usdc: float,
        fee_model: str,
        description: str | None = None,
        callback_url: str | None = None,
        credits_per_payment: int | None = None,
        duration_seconds: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "slug": slug,
            "type": type,
            "price_usdc": price_usdc,
            "fee_model": fee_model,
        }
        if description is not None:
            body["description"] = description
        if callback_url is not None:
            body["callback_url"] = callback_url
        if credits_per_payment is not None:
            body["credits_per_payment"] = credits_per_payment
        if duration_seconds is not None:
            body["duration_seconds"] = duration_seconds
        return self._request("POST", "/resources", body)

    def list_my_resources(self) -> list[dict[str, Any]]:
        return self._request("GET", "/resources")

    def get_analytics(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        qs = f"?{urlencode(params)}" if params else ""
        return self._request("GET", f"/analytics{qs}")

    def list_payments(self) -> list[dict[str, Any]]:
        return self._request("GET", "/payments")

    # ------------------------------------------------------------------
    # Extended vendor tools
    # ------------------------------------------------------------------

    def create_vendor(
        self,
        *,
        name: str,
        description: str | None = None,
        website: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if website is not None:
            body["website"] = website
        return self._request("POST", "/vendors", body)

    def create_plan(
        self,
        *,
        resource_id: str,
        name: str,
        fee_model: str,
        price_usdc: float,
        credits_per_payment: int | None = None,
        duration_seconds: int | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "resource_id": resource_id,
            "name": name,
            "fee_model": fee_model,
            "price_usdc": price_usdc,
        }
        if credits_per_payment is not None:
            body["credits_per_payment"] = credits_per_payment
        if duration_seconds is not None:
            body["duration_seconds"] = duration_seconds
        if description is not None:
            body["description"] = description
        return self._request("POST", "/plans", body)

    def create_subscription(
        self,
        *,
        resource_id: str,
        payer_wallet: str,
        plan_id: str | None = None,
        coupon_code: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "resource_id": resource_id,
            "payer_wallet": payer_wallet,
        }
        if plan_id is not None:
            body["plan_id"] = plan_id
        if coupon_code is not None:
            body["coupon_code"] = coupon_code
        return self._request("POST", "/subscriptions", body)

    def get_earnings(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        resource_id: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if resource_id:
            params["resource_id"] = resource_id
        qs = f"?{urlencode(params)}" if params else ""
        return self._request("GET", f"/analytics{qs}")
