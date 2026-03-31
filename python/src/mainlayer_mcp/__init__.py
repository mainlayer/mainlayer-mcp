"""
mainlayer-mcp — MCP server for Mainlayer payment infrastructure.

Exposes buyer and vendor tools so any MCP-compatible AI agent can
discover, pay for, and sell resources via Mainlayer.
"""

__version__ = "0.1.0"
__all__ = ["create_server"]

from .server import create_server
