"""
Vendor tools — for agents that sell resources via Mainlayer.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import MainlayerClient


def register_vendor_tools(mcp: FastMCP, client: MainlayerClient) -> None:
    """Register all vendor tools on the FastMCP server instance."""

    @mcp.tool()
    def create_resource(
        slug: str,
        type: str,
        price_usdc: float,
        fee_model: str,
        description: str | None = None,
        callback_url: str | None = None,
        credits_per_payment: int | None = None,
        duration_seconds: int | None = None,
    ) -> dict[str, Any]:
        """Create a new paid resource on Mainlayer that other agents can purchase.

        Returns the created resource including its assigned ID. Requires a valid
        MAINLAYER_API_KEY with vendor permissions.

        Args:
            slug: A URL-friendly unique identifier (e.g. 'my-api-v1').
            type: Resource type. One of: api, file, endpoint, page.
            price_usdc: Price per access in USD (e.g. 0.01 for one cent).
            fee_model: Pricing model. One of: one_time, subscription, pay_per_call.
            description: Human-readable description of what the resource provides.
            callback_url: Webhook URL called after a successful payment to deliver
                access or trigger fulfillment.
            credits_per_payment: For pay_per_call: number of API credits granted
                per payment.
            duration_seconds: For subscription: how long (in seconds) access lasts
                after payment.

        Returns:
            Created resource object with its assigned ID.
        """
        return client.create_resource(
            slug=slug,
            type=type,
            price_usdc=price_usdc,
            fee_model=fee_model,
            description=description,
            callback_url=callback_url,
            credits_per_payment=credits_per_payment,
            duration_seconds=duration_seconds,
        )

    @mcp.tool()
    def list_my_resources() -> list[dict[str, Any]]:
        """List all resources you have created on Mainlayer as a vendor.

        Returns resource IDs, slugs, types, prices, and fee models for all
        resources associated with your API key.

        Returns:
            List of resource objects.
        """
        return client.list_my_resources()

    @mcp.tool()
    def get_analytics(
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Retrieve revenue analytics for your Mainlayer resources.

        Returns total revenue, payment counts, and active subscriber counts.
        Optionally filter by date range.

        Args:
            start_date: Start of the analytics window in ISO 8601 format
                (e.g. '2024-01-01').
            end_date: End of the analytics window in ISO 8601 format
                (e.g. '2024-12-31').

        Returns:
            Analytics object with revenue stats.
        """
        return client.get_analytics(start_date=start_date, end_date=end_date)

    @mcp.tool()
    def list_payments() -> list[dict[str, Any]]:
        """View the full payment history for your Mainlayer vendor account.

        Returns all incoming payments with resource IDs, payer wallets, amounts,
        and statuses.

        Returns:
            List of payment objects.
        """
        return client.list_payments()
