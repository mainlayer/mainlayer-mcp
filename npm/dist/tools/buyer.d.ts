/**
 * Buyer tools — any agent can use these to discover and pay for resources.
 */
import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { MainlayerClient } from "../mainlayer.js";
export declare const buyerToolDefinitions: Tool[];
export declare function handleBuyerTool(name: string, args: Record<string, unknown>, client: MainlayerClient): Promise<unknown>;
//# sourceMappingURL=buyer.d.ts.map