# mainlayer-mcp (Python)

MCP server for [Mainlayer](https://mainlayer.fr) — give any AI agent the ability to discover, pay for, and sell resources via Mainlayer's payment infrastructure.

## Installation

```bash
pip install mainlayer-mcp
```

## Configuration

```bash
export MAINLAYER_API_KEY=ml_...
```

## Usage

```bash
python -m mainlayer_mcp
```

## Claude Desktop

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "python",
      "args": ["-m", "mainlayer_mcp"],
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
