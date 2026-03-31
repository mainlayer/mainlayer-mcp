#!/usr/bin/env node
/**
 * mainlayer-mcp — MCP server for Mainlayer payment infrastructure.
 *
 * Exposes buyer and vendor tools so any MCP-compatible AI agent can
 * discover, pay for, and sell resources via Mainlayer.
 *
 * Configuration:
 *   MAINLAYER_API_KEY  — Your Mainlayer API key (required)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import { MainlayerClient } from "./mainlayer.js";
import { buyerToolDefinitions, handleBuyerTool } from "./tools/buyer.js";
import { vendorToolDefinitions, handleVendorTool } from "./tools/vendor.js";

const TOOL_NAMES = new Set([
  ...buyerToolDefinitions.map((t) => t.name),
  ...vendorToolDefinitions.map((t) => t.name),
]);

const BUYER_TOOL_NAMES = new Set(buyerToolDefinitions.map((t) => t.name));
const VENDOR_TOOL_NAMES = new Set(vendorToolDefinitions.map((t) => t.name));

function getApiKey(): string {
  const key = process.env.MAINLAYER_API_KEY;
  if (!key) {
    console.error(
      "Error: MAINLAYER_API_KEY environment variable is not set.\n" +
        "Set it with: export MAINLAYER_API_KEY=ml_..."
    );
    process.exit(1);
  }
  return key;
}

async function main(): Promise<void> {
  const apiKey = getApiKey();
  const client = new MainlayerClient({ apiKey });

  const server = new Server(
    {
      name: "mainlayer-mcp",
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List all available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [...buyerToolDefinitions, ...vendorToolDefinitions],
    };
  });

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (!TOOL_NAMES.has(name)) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Unknown tool: ${name}` }),
          },
        ],
        isError: true,
      };
    }

    try {
      const safeArgs = (args ?? {}) as Record<string, unknown>;
      let result: unknown;

      if (BUYER_TOOL_NAMES.has(name)) {
        result = await handleBuyerTool(name, safeArgs, client);
      } else if (VENDOR_TOOL_NAMES.has(name)) {
        result = await handleVendorTool(name, safeArgs, client);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: message }),
          },
        ],
        isError: true,
      };
    }
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Mainlayer MCP server running on stdio");
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
