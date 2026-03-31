/**
 * Buyer tools — any agent can use these to discover and pay for resources.
 */
export const buyerToolDefinitions = [
    {
        name: "discover_resources",
        description: "Search for available paid resources on the Mainlayer marketplace. " +
            "Returns a list of resources with their IDs, slugs, descriptions, prices, and fee models. " +
            "Use this before paying for a resource to find the right resource_id.",
        inputSchema: {
            type: "object",
            properties: {
                query: {
                    type: "string",
                    description: "Free-text search query to filter resources by name or description.",
                },
                type: {
                    type: "string",
                    enum: ["api", "file", "endpoint", "page"],
                    description: "Filter by resource type.",
                },
                fee_model: {
                    type: "string",
                    enum: ["one_time", "subscription", "pay_per_call"],
                    description: "Filter by pricing model.",
                },
                limit: {
                    type: "number",
                    description: "Maximum number of results to return (default: 20).",
                },
            },
        },
    },
    {
        name: "get_resource_info",
        description: "Get detailed information about a specific Mainlayer resource by its ID. " +
            "Returns full details including price, fee model, description, and callback URL.",
        inputSchema: {
            type: "object",
            properties: {
                resource_id: {
                    type: "string",
                    description: "The unique identifier of the resource.",
                },
            },
            required: ["resource_id"],
        },
    },
    {
        name: "pay_for_resource",
        description: "Execute a Mainlayer payment to purchase access to a resource. " +
            "Returns a payment confirmation along with entitlement details such as expiry or remaining credits. " +
            "Use check_access first to avoid duplicate payments.",
        inputSchema: {
            type: "object",
            properties: {
                resource_id: {
                    type: "string",
                    description: "The unique identifier of the resource to pay for.",
                },
                payer_wallet: {
                    type: "string",
                    description: "The wallet address of the payer.",
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
        name: "check_access",
        description: "Check whether a wallet already has access to a specific Mainlayer resource. " +
            "Returns has_access (boolean), optional expiry timestamp, and remaining credits if applicable. " +
            "Always call this before pay_for_resource to avoid double-charging.",
        inputSchema: {
            type: "object",
            properties: {
                resource_id: {
                    type: "string",
                    description: "The unique identifier of the resource.",
                },
                payer_wallet: {
                    type: "string",
                    description: "The wallet address to check access for.",
                },
            },
            required: ["resource_id", "payer_wallet"],
        },
    },
];
export async function handleBuyerTool(name, args, client) {
    switch (name) {
        case "discover_resources": {
            const resources = await client.discoverResources({
                query: args.query,
                type: args.type,
                fee_model: args.fee_model,
                limit: args.limit,
            });
            return resources;
        }
        case "get_resource_info": {
            const resource = await client.getResourceInfo(args.resource_id);
            return resource;
        }
        case "pay_for_resource": {
            const payment = await client.payForResource({
                resource_id: args.resource_id,
                payer_wallet: args.payer_wallet,
                coupon_code: args.coupon_code,
            });
            return payment;
        }
        case "check_access": {
            const entitlement = await client.checkAccess({
                resource_id: args.resource_id,
                payer_wallet: args.payer_wallet,
            });
            return entitlement;
        }
        default:
            throw new Error(`Unknown buyer tool: ${name}`);
    }
}
//# sourceMappingURL=buyer.js.map