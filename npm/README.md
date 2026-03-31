# @mainlayer/mcp

MCP server for [Mainlayer](https://mainlayer.fr) — give any AI agent the ability to discover, pay for, and sell resources via Mainlayer's payment infrastructure.

## Installation

```bash
npm install -g @mainlayer/mcp
```

Or run without installing:

```bash
npx @mainlayer/mcp
```

## Configuration

```bash
export MAINLAYER_API_KEY=ml_...
```

## Claude Desktop

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "npx",
      "args": ["@mainlayer/mcp"],
      "env": {
        "MAINLAYER_API_KEY": "ml_..."
      }
    }
  }
}
```

## Tools

**Buyer tools:** `discover_resources`, `get_resource_info`, `pay_for_resource`, `check_access`

**Vendor tools:** `create_resource`, `list_my_resources`, `get_analytics`, `list_payments`

See the [main README](../README.md) for full documentation.
