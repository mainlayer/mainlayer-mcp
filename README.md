# mainlayer-mcp

MCP server for [Mainlayer](https://mainlayer.fr) — give any AI agent the ability to discover, pay for, and sell resources via Mainlayer's payment infrastructure.

Full documentation at [docs.mainlayer.fr](https://docs.mainlayer.fr).

Available as:
- **`@mainlayer/mcp`** on npm (TypeScript/Node.js)
- **`mainlayer-mcp`** on PyPI (Python)

---

## What is Mainlayer?

Mainlayer is payment infrastructure built for AI agents. Any agent can discover paid resources, execute payments, check entitlements, manage subscriptions, and earn revenue — all without human intervention.

---

## Installation

### npm (recommended for Claude Desktop)

Run without installing:

```bash
npx -y @mainlayer/mcp
```

Or install globally:

```bash
npm install -g @mainlayer/mcp
mainlayer-mcp
```

### pip / uvx (Python)

```bash
pip install mainlayer-mcp
python -m mainlayer_mcp
```

Or with `uvx`:

```bash
uvx mainlayer-mcp
```

---

## Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

**Using npm (recommended):**

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

**Using Python (uvx):**

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "uvx",
      "args": ["mainlayer-mcp"],
      "env": {
        "MAINLAYER_API_KEY": "ml_your_api_key_here"
      }
    }
  }
}
```

**Using Python (pip):**

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "python",
      "args": ["-m", "mainlayer_mcp"],
      "env": {
        "MAINLAYER_API_KEY": "ml_your_api_key_here"
      }
    }
  }
}
```

Get your API key at [mainlayer.fr](https://mainlayer.fr).

---

## Available MCP Tools

### Vendor tools — earn revenue by selling resources

| Tool | Description |
|------|-------------|
| `create_vendor` | Register as a vendor on Mainlayer |
| `create_resource` | Create a new billable resource (API, file, endpoint, page) |
| `list_resources` | List all your vendor resources |
| `create_plan` | Create a pricing plan for a resource |
| `get_earnings` | Get revenue analytics with optional date/resource filters |
| `create_subscription` | Set up a recurring subscription for a payer |
| `get_analytics` | Get full analytics for your resources |
| `list_payments` | View complete incoming payment history |

### Buyer tools — discover and pay for resources

| Tool | Description |
|------|-------------|
| `discover_resources` | Search the Mainlayer marketplace |
| `get_resource_info` | Get full details about a resource by ID |
| `check_access` | Check whether a wallet has active access |
| `pay_for_resource` | Execute a payment to purchase access |

---

## Example Prompts to Claude

Once configured, try these prompts in Claude Desktop:

**As a vendor:**
- "Register me as a vendor on Mainlayer with the name 'My AI Services'."
- "Create a paid API called 'Stock Sentiment API' at $0.02 per call."
- "Add a Pro pricing plan at $0.05/call with 50 credits per payment."
- "How much have I earned on Mainlayer this month?"
- "List all my resources on Mainlayer."

**As a buyer:**
- "Find me a weather API on Mainlayer."
- "Check if my wallet 0x... has access to resource res_abc123."
- "Pay for resource res_abc123 using wallet 0x..."
- "Subscribe my wallet to the monthly plan for res_abc123."

See [`examples/example_conversations.md`](./examples/example_conversations.md) for full conversation examples.

---

## Configuration

Set your API key via environment variable:

```bash
export MAINLAYER_API_KEY=ml_...
```

### Other MCP clients (Cursor, VS Code, etc.)

Add to `.cursor/mcp.json` or your client's config:

```json
{
  "mcpServers": {
    "mainlayer": {
      "command": "npx",
      "args": ["-y", "@mainlayer/mcp"],
      "env": {
        "MAINLAYER_API_KEY": "ml_..."
      }
    }
  }
}
```

---

## Example agent workflows

### Earn money: register and monetize a service

```
You: Create a paid API called "Earnings Forecast API" at $0.05 per call.

Claude calls: create_vendor → create_resource → confirm resource is live
```

### Discover and pay for a resource

```
Claude calls: discover_resources({ query: "weather forecast API" })
→ [{ id: "res_abc123", slug: "weather-api", price_usdc: 0.01, fee_model: "pay_per_call" }]

Claude calls: check_access({ resource_id: "res_abc123", payer_wallet: "wallet_xyz" })
→ { has_access: false }

Claude calls: pay_for_resource({ resource_id: "res_abc123", payer_wallet: "wallet_xyz" })
→ { id: "pay_def456", status: "success", entitlement: { has_access: true, credits_remaining: 100 } }
```

### Create a resource with multiple pricing tiers

```
Claude calls: create_resource({ slug: "my-api", type: "api", price_usdc: 0.01, fee_model: "pay_per_call" })
→ { id: "res_new123", ... }

Claude calls: create_plan({ resource_id: "res_new123", name: "Pro", fee_model: "pay_per_call", price_usdc: 0.05, credits_per_payment: 50 })
→ { id: "plan_pro_001", ... }
```

---

## API Reference

Both packages call the Mainlayer REST API at `https://api.mainlayer.fr`.

- Full API docs: [docs.mainlayer.fr](https://docs.mainlayer.fr)

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

### Running tests

```bash
cd python
pip install -e ".[dev]"
pytest tests/
```

---

## License

MIT
