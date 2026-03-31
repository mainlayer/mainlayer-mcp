"""
Buyer tools — any agent can use these to discover and pay for resources.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import MainlayerClient


def register_buyer_tools(mcp: FastMCP, client: MainlayerClient) -> None:
    """Register all buyer tools on the FastMCP server instance."""

    @mcp.tool()
    def discover_resources(
        query: str | None = None,
        type: str | None = None,
        fee_model: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Search for available paid resources on the Mainlayer marketplace.

        Returns a list of resources with their IDs, slugs, descriptions, prices,
        and fee models. Use this before paying for a resource to find the right
        resource_id.

        Args:
            query: Free-text search query to filter resources by name or description.
            type: Filter by resource type. One of: api, file, endpoint, page.
            fee_model: Filter by pricing model. One of: one_time, subscription, pay_per_call.
            limit: Maximum number of results to return (default: 20).

        Returns:
            List of resource objects.
        """
        return client.discover_resources(
            query=query,
            type=type,
            fee_model=fee_model,
            limit=limit,
        )

    @mcp.tool()
    def get_resource_info(resource_id: str) -> dict[str, Any]:
        """Get detailed information about a specific Mainlayer resource by its ID.

        Returns full details including price, fee model, description, and callback URL.

        Args:
            resource_id: The unique identifier of the resource.

        Returns:
            Resource object with all fields.
        """
        return client.get_resource_info(resource_id)

    @mcp.tool()
    def pay_for_resource(
        resource_id: str,
        payer_wallet: str,
        coupon_code: str | None = None,
    ) -> dict[str, Any]:
        """Execute a Mainlayer payment to purchase access to a resource.

        Returns a payment confirmation along with entitlement details such as
        expiry timestamp or remaining credits. Use check_access first to avoid
        duplicate payments.

        Args:
            resource_id: The unique identifier of the resource to pay for.
            payer_wallet: The wallet address of the payer.
            coupon_code: Optional coupon or discount code.

        Returns:
            Payment confirmation with entitlement details.
        """
        return client.pay_for_resource(
            resource_id=resource_id,
            payer_wallet=payer_wallet,
            coupon_code=coupon_code,
        )

    @mcp.tool()
    def check_access(resource_id: str, payer_wallet: str) -> dict[str, Any]:
        """Check whether a wallet already has access to a specific Mainlayer resource.

        Returns has_access (boolean), optional expiry timestamp, and remaining
        credits if applicable. Always call this before pay_for_resource to avoid
        double-charging.

        Args:
            resource_id: The unique identifier of the resource.
            payer_wallet: The wallet address to check access for.

        Returns:
            Dict with has_access, expires_at (optional), credits_remaining (optional).
        """
        return client.check_access(
            resource_id=resource_id,
            payer_wallet=payer_wallet,
        )
