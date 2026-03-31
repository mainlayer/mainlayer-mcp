# @mainlayer/mcp

MCP server for [Mainlayer](https://mainlayer.fr) — give any AI agent the ability to discover, pay for, and sell resources via Mainlayer's payment infrastructure.

Full documentation at [docs.mainlayer.fr](https://docs.mainlayer.fr).

## Installation

Run without installing (recommended):

```bash
npx -y @mainlayer/mcp
```

Or install globally:

```bash
npm install -g @mainlayer/mcp
mainlayer-mcp
```

## Configuration

```bash
export MAINLAYER_API_KEY=ml_...
```

Get your API key at [mainlayer.fr](https://mainlayer.fr).

## Claude Desktop

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "npx",
      "args": ["-y", "@mainlayer/mcp"],
      "env": {
        "MAINLAYER_API_KEY": "ml_your_api_key_here"
      }
    }
  }
}
```

## Tools

**Vendor tools:** `create_vendor`, `create_resource`, `list_my_resources`, `create_plan`, `get_earnings`, `create_subscription`, `get_analytics`, `list_payments`

**Buyer tools:** `discover_resources`, `get_resource_info`, `check_access`, `pay_for_resource`

See the [main README](../README.md) for full documentation and examples.
