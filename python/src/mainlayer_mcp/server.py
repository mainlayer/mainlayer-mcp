"""
Mainlayer MCP server entry point.

Configuration:
    MAINLAYER_API_KEY  — Your Mainlayer API key (required)
"""

from __future__ import annotations

import os
import sys

from mcp.server.fastmcp import FastMCP

from .client import MainlayerClient
from .buyer import register_buyer_tools
from .vendor import register_vendor_tools


def create_server() -> FastMCP:
    """Create and configure the Mainlayer MCP server.

    Reads MAINLAYER_API_KEY from the environment and registers all buyer
    and vendor tools.

    Returns:
        Configured FastMCP server instance.

    Raises:
        SystemExit: If MAINLAYER_API_KEY is not set.
    """
    api_key = os.environ.get("MAINLAYER_API_KEY")
    if not api_key:
        print(
            "Error: MAINLAYER_API_KEY environment variable is not set.\n"
            "Set it with: export MAINLAYER_API_KEY=ml_...",
            file=sys.stderr,
        )
        sys.exit(1)

    client = MainlayerClient(api_key)

    mcp = FastMCP(
        "mainlayer-mcp",
        version="0.1.0",
        description=(
            "Mainlayer payment tools for AI agents. "
            "Discover, pay for, and sell resources programmatically."
        ),
    )

    register_buyer_tools(mcp, client)
    register_vendor_tools(mcp, client)

    return mcp


def main() -> None:
    """Run the Mainlayer MCP server over stdio."""
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()
