/**
 * Vendor tools — for agents that sell resources via Mainlayer.
 */
export const vendorToolDefinitions = [
    {
        name: "create_resource",
        description: "Create a new paid resource on Mainlayer that other agents (or users) can purchase. " +
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
                    description: "Webhook URL that Mainlayer will call after a successful payment " +
                        "to deliver access or trigger fulfillment.",
                },
                credits_per_payment: {
                    type: "number",
                    description: "For pay_per_call resources: number of API call credits granted per payment.",
                },
                duration_seconds: {
                    type: "number",
                    description: "For subscription resources: how long (in seconds) access lasts after payment.",
                },
            },
            required: ["slug", "type", "price_usdc", "fee_model"],
        },
    },
    {
        name: "list_my_resources",
        description: "List all resources you have created on Mainlayer as a vendor. " +
            "Returns resource IDs, slugs, types, prices, and fee models.",
        inputSchema: {
            type: "object",
            properties: {},
        },
    },
    {
        name: "get_analytics",
        description: "Retrieve revenue analytics for your Mainlayer resources. " +
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
        description: "View the full payment history for your Mainlayer vendor account. " +
            "Returns all incoming payments with resource IDs, payer wallets, amounts, and statuses.",
        inputSchema: {
            type: "object",
            properties: {},
        },
    },
];
export async function handleVendorTool(name, _args, client) {
    const args = _args;
    switch (name) {
        case "create_resource": {
            const resource = await client.createResource({
                slug: args.slug,
                type: args.type,
                price_usdc: args.price_usdc,
                fee_model: args.fee_model,
                description: args.description,
                callback_url: args.callback_url,
                credits_per_payment: args.credits_per_payment,
                duration_seconds: args.duration_seconds,
            });
            return resource;
        }
        case "list_my_resources": {
            const resources = await client.listMyResources();
            return resources;
        }
        case "get_analytics": {
            const analytics = await client.getAnalytics({
                start_date: args.start_date,
                end_date: args.end_date,
            });
            return analytics;
        }
        case "list_payments": {
            const payments = await client.listPayments();
            return payments;
        }
        default:
            throw new Error(`Unknown vendor tool: ${name}`);
    }
}
//# sourceMappingURL=vendor.js.map