"""Tests for all Mainlayer MCP tools using mocked HTTP."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from io import BytesIO

import pytest

from mainlayer_mcp.client import MainlayerClient, MainlayerError

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

API_KEY = "ml_test_key"
RESOURCE_ID = "res_abc123"
PAYER_WALLET = "0xdeadbeef"

SAMPLE_RESOURCES = [
    {
        "id": "res_abc123",
        "slug": "weather-api",
        "type": "api",
        "price_usdc": 0.01,
        "fee_model": "pay_per_call",
        "description": "Real-time weather data",
    },
    {
        "id": "res_def456",
        "slug": "news-feed",
        "type": "api",
        "price_usdc": 9.99,
        "fee_model": "subscription",
        "description": "Global news feed",
    },
]

SAMPLE_RESOURCE = SAMPLE_RESOURCES[0]

SAMPLE_PAYMENT = {
    "id": "pay_xyz789",
    "resource_id": RESOURCE_ID,
    "payer_wallet": PAYER_WALLET,
    "amount": 0.01,
    "status": "success",
    "entitlement": {"has_access": True, "credits_remaining": 100},
}

SAMPLE_ENTITLEMENT = {
    "has_access": True,
    "expires_at": "2027-01-01T00:00:00Z",
    "credits_remaining": 99,
}

SAMPLE_VENDOR = {
    "id": "vendor_001",
    "name": "My AI Services",
    "status": "active",
}

SAMPLE_CREATED_RESOURCE = {
    "id": "res_new001",
    "slug": "my-sentiment-api",
    "type": "api",
    "price_usdc": 0.02,
    "fee_model": "pay_per_call",
    "status": "active",
}

SAMPLE_PLAN = {
    "id": "plan_001",
    "resource_id": RESOURCE_ID,
    "name": "Pro",
    "fee_model": "pay_per_call",
    "price_usdc": 0.05,
    "credits_per_payment": 20,
}

SAMPLE_SUBSCRIPTION = {
    "id": "sub_001",
    "resource_id": RESOURCE_ID,
    "payer_wallet": PAYER_WALLET,
    "status": "active",
    "next_billing_at": "2026-04-30T00:00:00Z",
}

SAMPLE_ANALYTICS = {
    "total_revenue": 4567.89,
    "payment_count": 12345,
    "active_subscribers": 42,
    "resources": [
        {"resource_id": RESOURCE_ID, "revenue": 4567.89, "payments": 12345}
    ],
}

SAMPLE_PAYMENTS = [
    {
        "id": "pay_001",
        "resource_id": RESOURCE_ID,
        "payer_wallet": PAYER_WALLET,
        "amount": 0.01,
        "status": "success",
    }
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_urlopen(data: object, status: int = 200):
    """Context manager that mocks urllib.request.urlopen."""
    body = json.dumps(data).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return patch(
        "mainlayer_mcp.client.urlopen",
        return_value=mock_resp,
    )


def _mock_urlopen_error(status: int, message: str, body: dict | None = None):
    """Context manager that mocks urlopen to raise HTTPError."""
    error_body = json.dumps(body or {"error": message}).encode()
    exc = HTTPError(
        url="https://api.mainlayer.fr/test",
        code=status,
        msg=message,
        hdrs=None,  # type: ignore[arg-type]
        fp=BytesIO(error_body),
    )
    return patch("mainlayer_mcp.client.urlopen", side_effect=exc)


# ---------------------------------------------------------------------------
# Buyer tools
# ---------------------------------------------------------------------------


class TestDiscoverResources:
    def test_returns_resources(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_RESOURCES):
            result = client.discover_resources(query="weather")
        assert len(result) == 2
        assert result[0]["id"] == "res_abc123"

    def test_with_filters(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_RESOURCES) as mock_open:
            client.discover_resources(query="news", type="api", fee_model="subscription", limit=5)
        call_args = mock_open.call_args[0][0]
        assert "type=api" in call_args.full_url
        assert "fee_model=subscription" in call_args.full_url

    def test_http_error_raises(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen_error(401, "Unauthorized"):
            with pytest.raises(MainlayerError) as exc_info:
                client.discover_resources()
        assert exc_info.value.status == 401


class TestGetResourceInfo:
    def test_returns_resource(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_RESOURCE):
            result = client.get_resource_info(RESOURCE_ID)
        assert result["id"] == RESOURCE_ID
        assert result["slug"] == "weather-api"


class TestPayForResource:
    def test_returns_payment(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_PAYMENT):
            result = client.pay_for_resource(
                resource_id=RESOURCE_ID, payer_wallet=PAYER_WALLET
            )
        assert result["status"] == "success"
        assert result["entitlement"]["has_access"] is True

    def test_with_coupon(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_PAYMENT) as mock_open:
            client.pay_for_resource(
                resource_id=RESOURCE_ID,
                payer_wallet=PAYER_WALLET,
                coupon_code="DISCOUNT10",
            )
        call_args = mock_open.call_args[0][0]
        body = json.loads(call_args.data.decode())
        assert body["coupon_code"] == "DISCOUNT10"


class TestCheckAccess:
    def test_returns_entitlement(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_ENTITLEMENT):
            result = client.check_access(
                resource_id=RESOURCE_ID, payer_wallet=PAYER_WALLET
            )
        assert result["has_access"] is True
        assert result["credits_remaining"] == 99


# ---------------------------------------------------------------------------
# Vendor tools
# ---------------------------------------------------------------------------


class TestCreateVendor:
    def test_creates_vendor(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_VENDOR):
            result = client.create_vendor(name="My AI Services")
        assert result["id"] == "vendor_001"
        assert result["status"] == "active"

    def test_with_optional_fields(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_VENDOR) as mock_open:
            client.create_vendor(
                name="My AI Services",
                description="Premium AI data services",
                website="https://myaiservices.example.com",
            )
        call_args = mock_open.call_args[0][0]
        body = json.loads(call_args.data.decode())
        assert body["description"] == "Premium AI data services"
        assert body["website"] == "https://myaiservices.example.com"


class TestCreateResource:
    def test_creates_resource(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_CREATED_RESOURCE):
            result = client.create_resource(
                slug="my-sentiment-api",
                type="api",
                price_usdc=0.02,
                fee_model="pay_per_call",
                description="Sentiment analysis API",
            )
        assert result["id"] == "res_new001"
        assert result["status"] == "active"


class TestListMyResources:
    def test_returns_resources(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_RESOURCES):
            result = client.list_my_resources()
        assert len(result) == 2


class TestCreatePlan:
    def test_creates_plan(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_PLAN):
            result = client.create_plan(
                resource_id=RESOURCE_ID,
                name="Pro",
                fee_model="pay_per_call",
                price_usdc=0.05,
                credits_per_payment=20,
            )
        assert result["id"] == "plan_001"
        assert result["credits_per_payment"] == 20

    def test_sends_correct_fields(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_PLAN) as mock_open:
            client.create_plan(
                resource_id=RESOURCE_ID,
                name="Pro",
                fee_model="pay_per_call",
                price_usdc=0.05,
            )
        call_args = mock_open.call_args[0][0]
        body = json.loads(call_args.data.decode())
        assert body["resource_id"] == RESOURCE_ID
        assert body["fee_model"] == "pay_per_call"
        assert body["price_usdc"] == 0.05


class TestCreateSubscription:
    def test_creates_subscription(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_SUBSCRIPTION):
            result = client.create_subscription(
                resource_id=RESOURCE_ID,
                payer_wallet=PAYER_WALLET,
            )
        assert result["id"] == "sub_001"
        assert result["status"] == "active"

    def test_with_plan_id(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_SUBSCRIPTION) as mock_open:
            client.create_subscription(
                resource_id=RESOURCE_ID,
                payer_wallet=PAYER_WALLET,
                plan_id="plan_001",
            )
        call_args = mock_open.call_args[0][0]
        body = json.loads(call_args.data.decode())
        assert body["plan_id"] == "plan_001"


class TestGetEarnings:
    def test_returns_analytics(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_ANALYTICS):
            result = client.get_earnings()
        assert result["total_revenue"] == 4567.89
        assert result["payment_count"] == 12345

    def test_with_date_filter(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_ANALYTICS) as mock_open:
            client.get_earnings(start_date="2024-01-01", end_date="2024-12-31")
        call_args = mock_open.call_args[0][0]
        assert "start_date=2024-01-01" in call_args.full_url

    def test_with_resource_filter(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_ANALYTICS) as mock_open:
            client.get_earnings(resource_id=RESOURCE_ID)
        call_args = mock_open.call_args[0][0]
        assert f"resource_id={RESOURCE_ID}" in call_args.full_url


class TestGetAnalytics:
    def test_returns_analytics(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_ANALYTICS):
            result = client.get_analytics()
        assert result["total_revenue"] == 4567.89


class TestListPayments:
    def test_returns_payments(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen(SAMPLE_PAYMENTS):
            result = client.list_payments()
        assert len(result) == 1
        assert result[0]["status"] == "success"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestErrorHandling:
    def test_http_error_with_json_body(self) -> None:
        client = MainlayerClient(API_KEY)
        with _mock_urlopen_error(422, "Unprocessable Entity", {"error": "Invalid slug format"}):
            with pytest.raises(MainlayerError) as exc_info:
                client.create_resource(
                    slug="invalid slug with spaces",
                    type="api",
                    price_usdc=0.01,
                    fee_model="pay_per_call",
                )
        assert "Invalid slug format" in str(exc_info.value)
        assert exc_info.value.status == 422

    def test_http_error_without_json_body(self) -> None:
        client = MainlayerClient(API_KEY)
        exc = HTTPError(
            url="https://api.mainlayer.fr/test",
            code=500,
            msg="Internal Server Error",
            hdrs=None,  # type: ignore[arg-type]
            fp=BytesIO(b"not json"),
        )
        with patch("mainlayer_mcp.client.urlopen", side_effect=exc):
            with pytest.raises(MainlayerError) as exc_info:
                client.discover_resources()
        assert exc_info.value.status == 500
