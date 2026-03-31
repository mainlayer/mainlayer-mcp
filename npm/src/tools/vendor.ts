/**
 * Vendor tools — for agents that sell resources via Mainlayer.
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { MainlayerClient } from "../mainlayer.js";

export const vendorToolDefinitions: Tool[] = [
  {
    name: "create_vendor",
    description:
      "Register as a vendor on Mainlayer. Creates a vendor profile that lets you list paid " +
      "resources and receive payments from buyers. Run this once before creating resources.",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Display name for your vendor profile.",
        },
        description: {
          type: "string",
          description: "Optional description of your business or services.",
        },
        website: {
          type: "string",
          description: "Optional URL for your website or API documentation.",
        },
      },
      required: ["name"],
    },
  },
  {
    name: "create_resource",
    description:
      "Create a new paid resource on Mainlayer that other agents (or users) can purchase. " +
      "Returns the created resource including its assigned ID. " +
      "Requires a valid MAINLAYER_API_KEY with vendor permissions.",
    inputSchema: {
      type: "object",
      properties: {
        slug: {
          type: "string",
          description: "A URL-friendly unique identifier for the resource (e.g. 'my-api-v1').",
        },
        type: {
          type: "string",
          enum: ["api", "file", "endpoint", "page"],
          description: "The type of resource being sold.",
        },
        price_usdc: {
          type: "number",
          description: "Price per access in USD (e.g. 0.01 for one cent).",
        },
        fee_model: {
          type: "string",
          enum: ["one_time", "subscription", "pay_per_call"],
          description: "The pricing model for the resource.",
        },
        description: {
          type: "string",
          description: "Human-readable description of what the resource provides.",
        },
        callback_url: {
          type: "string",
          description:
            "Webhook URL that Mainlayer will call after a successful payment " +
            "to deliver access or trigger fulfillment.",
        },
        credits_per_payment: {
          type: "number",
          description:
            "For pay_per_call resources: number of API call credits granted per payment.",
        },
        duration_seconds: {
          type: "number",
          description:
            "For subscription resources: how long (in seconds) access lasts after payment.",
        },
      },
      required: ["slug", "type", "price_usdc", "fee_model"],
    },
  },
  {
    name: "list_my_resources",
    description:
      "List all resources you have created on Mainlayer as a vendor. " +
      "Returns resource IDs, slugs, types, prices, and fee models.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "list_resources",
    description:
      "List all your resources on Mainlayer. " +
      "Alias for list_my_resources. Returns all resources associated with your API key.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "get_analytics",
    description:
      "Retrieve revenue analytics for your Mainlayer resources. " +
      "Returns total revenue, payment counts, and active subscriber counts. " +
      "Optionally filter by date range.",
    inputSchema: {
      type: "object",
      properties: {
        start_date: {
          type: "string",
          description: "Start of the analytics window in ISO 8601 format (e.g. '2024-01-01').",
        },
        end_date: {
          type: "string",
          description: "End of the analytics window in ISO 8601 format (e.g. '2024-12-31').",
        },
      },
    },
  },
  {
    name: "list_payments",
    description:
      "View the full payment history for your Mainlayer vendor account. " +
      "Returns all incoming payments with resource IDs, payer wallets, amounts, and statuses.",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "create_plan",
    description:
      "Create a pricing plan for an existing Mainlayer resource. " +
      "Use this to add pricing tiers (e.g. Basic at $0.01/call, Pro at $0.05/call). " +
      "A resource can have multiple plans.",
    inputSchema: {
      type: "object",
      properties: {
        resource_id: {
          type: "string",
          description: "The ID of the resource to add a plan to.",
        },
        name: {
          type: "string",
          description: "Display name for the plan (e.g. 'Basic', 'Pro').",
        },
        fee_model: {
          type: "string",
          enum: ["one_time", "subscription", "pay_per_call"],
          description: "The pricing model for this plan.",
        },
        price_usdc: {
          type: "number",
          description: "Price per access in USD.",
        },
        credits_per_payment: {
          type: "number",
          description: "For pay_per_call: API credits granted per payment.",
        },
        duration_seconds: {
          type: "number",
          description: "For subscription: seconds of access per payment.",
        },
        description: {
          type: "string",
          description: "Optional description of this plan's value.",
        },
      },
      required: ["resource_id", "name", "fee_model", "price_usdc"],
    },
  },
  {
    name: "create_subscription",
    description:
      "Set up a recurring subscription for a payer to access a resource. " +
      "The payer will be charged automatically each billing cycle without manual renewals.",
    inputSchema: {
      type: "object",
      properties: {
        resource_id: {
          type: "string",
          description: "The ID of the resource to subscribe to.",
        },
        payer_wallet: {
          type: "string",
          description: "The wallet address of the subscribing payer.",
        },
        plan_id: {
          type: "string",
          description: "Optional plan ID to select a specific pricing tier.",
        },
        coupon_code: {
          type: "string",
          description: "Optional coupon or discount code.",
        },
      },
      required: ["resource_id", "payer_wallet"],
    },
  },
  {
    name: "get_earnings",
    description:
      "Get revenue analytics and earnings for your Mainlayer resources. " +
      "Returns total earnings, payment counts, active subscribers, and per-resource breakdowns. " +
      "Optionally filter by date range or specific resource.",
    inputSchema: {
      type: "object",
      properties: {
        start_date: {
          type: "string",
          description: "Start of period in ISO 8601 format (e.g. '2024-01-01').",
        },
        end_date: {
          type: "string",
          description: "End of period in ISO 8601 format (e.g. '2024-12-31').",
        },
        resource_id: {
          type: "string",
          description: "Optional — filter analytics to a specific resource.",
        },
      },
    },
  },
];

export async function handleVendorTool(
  name: string,
  _args: Record<string, unknown>,
  client: MainlayerClient
): Promise<unknown> {
  const args = _args;

  switch (name) {
    case "create_vendor": {
      const vendor = await client.createVendor({
        name: args.name as string,
        description: args.description as string | undefined,
        website: args.website as string | undefined,
      });
      return vendor;
    }

    case "create_resource": {
      const resource = await client.createResource({
        slug: args.slug as string,
        type: args.type as string,
        price_usdc: args.price_usdc as number,
        fee_model: args.fee_model as string,
        description: args.description as string | undefined,
        callback_url: args.callback_url as string | undefined,
        credits_per_payment: args.credits_per_payment as number | undefined,
        duration_seconds: args.duration_seconds as number | undefined,
      });
      return resource;
    }

    case "list_my_resources":
    case "list_resources": {
      const resources = await client.listMyResources();
      return resources;
    }

    case "get_analytics": {
      const analytics = await client.getAnalytics({
        start_date: args.start_date as string | undefined,
        end_date: args.end_date as string | undefined,
      });
      return analytics;
    }

    case "list_payments": {
      const payments = await client.listPayments();
      return payments;
    }

    case "create_plan": {
      const plan = await client.createPlan({
        resource_id: args.resource_id as string,
        name: args.name as string,
        fee_model: args.fee_model as string,
        price_usdc: args.price_usdc as number,
        credits_per_payment: args.credits_per_payment as number | undefined,
        duration_seconds: args.duration_seconds as number | undefined,
        description: args.description as string | undefined,
      });
      return plan;
    }

    case "create_subscription": {
      const subscription = await client.createSubscription({
        resource_id: args.resource_id as string,
        payer_wallet: args.payer_wallet as string,
        plan_id: args.plan_id as string | undefined,
        coupon_code: args.coupon_code as string | undefined,
      });
      return subscription;
    }

    case "get_earnings": {
      const earnings = await client.getEarnings({
        start_date: args.start_date as string | undefined,
        end_date: args.end_date as string | undefined,
        resource_id: args.resource_id as string | undefined,
      });
      return earnings;
    }

    default:
      throw new Error(`Unknown vendor tool: ${name}`);
  }
}
