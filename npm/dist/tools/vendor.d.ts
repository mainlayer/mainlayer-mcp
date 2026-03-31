/**
 * Vendor tools — for agents that sell resources via Mainlayer.
 */
import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { MainlayerClient } from "../mainlayer.js";
export declare const vendorToolDefinitions: Tool[];
export declare function handleVendorTool(name: string, _args: Record<string, unknown>, client: MainlayerClient): Promise<unknown>;
//# sourceMappingURL=vendor.d.ts.map