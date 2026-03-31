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
    def list_resources() -> list[dict[str, Any]]:
        """List all your resources on Mainlayer.

        Alias for list_my_resources. Returns all resources associated with
        your API key including their IDs, slugs, types, prices, and statuses.

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

    @mcp.tool()
    def create_vendor(
        name: str,
        description: str | None = None,
        website: str | None = None,
    ) -> dict[str, Any]:
        """Register as a vendor on Mainlayer.

        Creates a vendor profile that lets you list paid resources and receive
        payments from buyers. Run this once before creating any resources.

        Args:
            name: Display name for your vendor profile.
            description: Optional description of your business or services.
            website: Optional URL for your website or API documentation.

        Returns:
            Created vendor profile with vendor ID.
        """
        return client.create_vendor(
            name=name,
            description=description,
            website=website,
        )

    @mcp.tool()
    def create_plan(
        resource_id: str,
        name: str,
        fee_model: str,
        price_usdc: float,
        credits_per_payment: int | None = None,
        duration_seconds: int | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a pricing plan for an existing Mainlayer resource.

        Use this to add or update pricing tiers for a resource. A resource can
        have multiple plans (e.g. basic at $0.01/call and pro at $0.05/call).

        Args:
            resource_id: The ID of the resource to add a plan to.
            name: Display name for the plan (e.g. 'Basic', 'Pro').
            fee_model: Pricing model. One of: one_time, subscription, pay_per_call.
            price_usdc: Price per access in USD.
            credits_per_payment: For pay_per_call: API credits granted per payment.
            duration_seconds: For subscription: seconds of access per payment.
            description: Optional description of this plan's value.

        Returns:
            Created plan object with plan ID.
        """
        return client.create_plan(
            resource_id=resource_id,
            name=name,
            fee_model=fee_model,
            price_usdc=price_usdc,
            credits_per_payment=credits_per_payment,
            duration_seconds=duration_seconds,
            description=description,
        )

    @mcp.tool()
    def create_subscription(
        resource_id: str,
        payer_wallet: str,
        plan_id: str | None = None,
        coupon_code: str | None = None,
    ) -> dict[str, Any]:
        """Set up a recurring subscription for a payer to access a resource.

        Initiates a subscription payment so the payer receives ongoing access
        without manual renewals. The payer will be charged each billing cycle.

        Args:
            resource_id: The ID of the resource to subscribe to.
            payer_wallet: The wallet address of the subscribing payer.
            plan_id: Optional plan ID to select a specific pricing tier.
            coupon_code: Optional coupon or discount code.

        Returns:
            Subscription object with subscription ID and next billing date.
        """
        return client.create_subscription(
            resource_id=resource_id,
            payer_wallet=payer_wallet,
            plan_id=plan_id,
            coupon_code=coupon_code,
        )

    @mcp.tool()
    def get_earnings(
        start_date: str | None = None,
        end_date: str | None = None,
        resource_id: str | None = None,
    ) -> dict[str, Any]:
        """Get revenue analytics and earnings for your Mainlayer resources.

        Returns total earnings, payment counts, active subscribers, and
        per-resource breakdowns. Optionally filter by date range or resource.

        Args:
            start_date: Start of period in ISO 8601 format (e.g. '2024-01-01').
            end_date: End of period in ISO 8601 format (e.g. '2024-12-31').
            resource_id: Optional — filter analytics to a specific resource.

        Returns:
            Analytics object with total_revenue, payment_count, active_subscribers,
            and per-resource breakdown.
        """
        return client.get_earnings(
            start_date=start_date,
            end_date=end_date,
            resource_id=resource_id,
        )
