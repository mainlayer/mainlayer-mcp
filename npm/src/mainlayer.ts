/**
 * Mainlayer API client
 * Wraps the Mainlayer payment infrastructure REST API.
 */

const BASE_URL = "https://api.mainlayer.xyz";

export interface MainlayerConfig {
  apiKey: string;
}

export interface Resource {
  id: string;
  slug: string;
  type: string;
  price_usdc: number;
  fee_model: string;
  description?: string;
  callback_url?: string;
  credits_per_payment?: number;
  duration_seconds?: number;
  created_at?: string;
}

export interface Payment {
  id: string;
  resource_id: string;
  payer_wallet: string;
  amount: number;
  status: string;
  created_at?: string;
  entitlement?: Entitlement;
}

export interface Entitlement {
  has_access: boolean;
  expires_at?: string;
  credits_remaining?: number;
}

export interface Analytics {
  total_revenue?: number;
  payment_count?: number;
  active_subscribers?: number;
  [key: string]: unknown;
}

export class MainlayerClient {
  private apiKey: string;

  constructor(config: MainlayerConfig) {
    this.apiKey = config.apiKey;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const url = `${BASE_URL}${path}`;
    const headers: Record<string, string> = {
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
        const errorBody = await response.json() as Record<string, unknown>;
        if (errorBody.error || errorBody.message) {
          errorMessage = (errorBody.error ?? errorBody.message) as string;
        }
      } catch {
        // ignore parse error, use default message
      }
      throw new Error(errorMessage);
    }

    return response.json() as Promise<T>;
  }

  // Buyer tools

  async discoverResources(params: {
    query?: string;
    type?: string;
    fee_model?: string;
    limit?: number;
  }): Promise<Resource[]> {
    const qs = new URLSearchParams();
    if (params.query) qs.set("q", params.query);
    if (params.type) qs.set("type", params.type);
    if (params.fee_model) qs.set("fee_model", params.fee_model);
    if (params.limit !== undefined) qs.set("limit", String(params.limit));
    const query = qs.toString();
    return this.request<Resource[]>("GET", `/discover${query ? `?${query}` : ""}`);
  }

  async getResourceInfo(resourceId: string): Promise<Resource> {
    return this.request<Resource>("GET", `/resources/public/${resourceId}`);
  }

  async payForResource(params: {
    resource_id: string;
    payer_wallet: string;
    coupon_code?: string;
  }): Promise<Payment> {
    return this.request<Payment>("POST", "/pay", params);
  }

  async checkAccess(params: {
    resource_id: string;
    payer_wallet: string;
  }): Promise<Entitlement> {
    const qs = new URLSearchParams({
      resource_id: params.resource_id,
      payer_wallet: params.payer_wallet,
    });
    return this.request<Entitlement>("GET", `/entitlements/check?${qs}`);
  }

  // Vendor tools

  async createResource(params: {
    slug: string;
    type: string;
    price_usdc: number;
    fee_model: string;
    description?: string;
    callback_url?: string;
    credits_per_payment?: number;
    duration_seconds?: number;
  }): Promise<Resource> {
    return this.request<Resource>("POST", "/resources", params);
  }

  async listMyResources(): Promise<Resource[]> {
    return this.request<Resource[]>("GET", "/resources");
  }

  async getAnalytics(params: {
    start_date?: string;
    end_date?: string;
  }): Promise<Analytics> {
    const qs = new URLSearchParams();
    if (params.start_date) qs.set("start_date", params.start_date);
    if (params.end_date) qs.set("end_date", params.end_date);
    const query = qs.toString();
    return this.request<Analytics>("GET", `/analytics${query ? `?${query}` : ""}`);
  }

  async listPayments(): Promise<Payment[]> {
    return this.request<Payment[]>("GET", "/payments");
  }
}
