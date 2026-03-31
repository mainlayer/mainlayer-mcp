# mainlayer-mcp

MCP server for [Mainlayer](https://mainlayer.fr) — give any AI agent the ability to discover, pay for, and sell resources via Mainlayer's payment infrastructure.

Available as:
- **`@mainlayer/mcp`** on npm (TypeScript/Node.js)
- **`mainlayer-mcp`** on PyPI (Python)

---

## What is Mainlayer?

Mainlayer is payment infrastructure built for AI agents. Any agent can discover paid resources, execute payments, check entitlements, and manage subscriptions — all without human intervention.

---

## Tools

### Buyer tools (any agent can use these)

| Tool | Description |
|---|---|
| `discover_resources` | Search the Mainlayer marketplace for available paid resources |
| `get_resource_info` | Get full details about a specific resource by ID |
| `pay_for_resource` | Execute a payment to purchase access |
| `check_access` | Check whether a wallet already has access to a resource |

### Vendor tools (for agents selling things)

| Tool | Description |
|---|---|
| `create_resource` | Create a new paid resource on Mainlayer |
| `list_my_resources` | List all your vendor resources |
| `get_analytics` | Get revenue analytics, optionally filtered by date |
| `list_payments` | View full incoming payment history |

---

## Installation

### npm (TypeScript/Node.js)

```bash
npx @mainlayer/mcp
```

Or install globally:

```bash
npm install -g @mainlayer/mcp
mainlayer-mcp
```

### pip (Python)

```bash
pip install mainlayer-mcp
python -m mainlayer_mcp
```

---

## Configuration

Set your API key via environment variable:

```bash
export MAINLAYER_API_KEY=ml_...
```

Get your API key at [mainlayer.fr](https://mainlayer.fr).

---

## Client Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

**Using npm (npx):**

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

**Using Python:**

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

### Cursor

Add to `.cursor/mcp.json` in your project root or `~/.cursor/mcp.json` globally:

**Using npm:**

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

**Using Python:**

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

### Generic MCP client

Any MCP-compatible client that supports stdio transport can connect to this server.

**npm:**

```bash
MAINLAYER_API_KEY=ml_... npx @mainlayer/mcp
```

**Python:**

```bash
MAINLAYER_API_KEY=ml_... python -m mainlayer_mcp
```

---

## Example agent workflows

### Discover and pay for a resource

```
Agent: discover_resources({ query: "weather forecast API" })
→ [{ id: "res_abc123", slug: "weather-api", price_usdc: 0.01, fee_model: "pay_per_call" }]

Agent: check_access({ resource_id: "res_abc123", payer_wallet: "wallet_xyz" })
→ { has_access: false }

Agent: pay_for_resource({ resource_id: "res_abc123", payer_wallet: "wallet_xyz" })
→ { id: "pay_def456", status: "success", entitlement: { has_access: true, credits_remaining: 100 } }
```

### Create and monetize a resource

```
Agent: create_resource({
  slug: "my-analysis-api",
  type: "api",
  price_usdc: 0.05,
  fee_model: "pay_per_call",
  description: "Financial data analysis endpoint",
  callback_url: "https://my-server.example.com/mainlayer/webhook",
  credits_per_payment: 10
})
→ { id: "res_new123", slug: "my-analysis-api", ... }
```

---

## Development

### npm package

```bash
cd npm
npm install
npm run build
npm start
```

### Python package

```bash
cd python
pip install -e ".[dev]"
python -m mainlayer_mcp
```

---

## License

MIT — see [LICENSE](LICENSE).
