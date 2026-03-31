/**
 * Mainlayer API client
 * Wraps the Mainlayer payment infrastructure REST API.
 */
const BASE_URL = "https://api.mainlayer.xyz";
export class MainlayerClient {
    apiKey;
    constructor(config) {
        this.apiKey = config.apiKey;
    }
    async request(method, path, body) {
        const url = `${BASE_URL}${path}`;
        const headers = {
            Authorization: `Bearer ${this.apiKey}`,
            "Content-Type": "application/json",
        };
        const response = await fetch(url, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });
        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            try {
                const errorBody = await response.json();
                if (errorBody.error || errorBody.message) {
                    errorMessage = (errorBody.error ?? errorBody.message);
                }
            }
            catch {
                // ignore parse error, use default message
            }
            throw new Error(errorMessage);
        }
        return response.json();
    }
    // Buyer tools
    async discoverResources(params) {
        const qs = new URLSearchParams();
        if (params.query)
            qs.set("q", params.query);
        if (params.type)
            qs.set("type", params.type);
        if (params.fee_model)
            qs.set("fee_model", params.fee_model);
        if (params.limit !== undefined)
            qs.set("limit", String(params.limit));
        const query = qs.toString();
        return this.request("GET", `/discover${query ? `?${query}` : ""}`);
    }
    async getResourceInfo(resourceId) {
        return this.request("GET", `/resources/public/${resourceId}`);
    }
    async payForResource(params) {
        return this.request("POST", "/pay", params);
    }
    async checkAccess(params) {
        const qs = new URLSearchParams({
            resource_id: params.resource_id,
            payer_wallet: params.payer_wallet,
        });
        return this.request("GET", `/entitlements/check?${qs}`);
    }
    // Vendor tools
    async createResource(params) {
        return this.request("POST", "/resources", params);
    }
    async listMyResources() {
        return this.request("GET", "/resources");
    }
    async getAnalytics(params) {
        const qs = new URLSearchParams();
        if (params.start_date)
            qs.set("start_date", params.start_date);
        if (params.end_date)
            qs.set("end_date", params.end_date);
        const query = qs.toString();
        return this.request("GET", `/analytics${query ? `?${query}` : ""}`);
    }
    async listPayments() {
        return this.request("GET", "/payments");
    }
}
//# sourceMappingURL=mainlayer.js.map