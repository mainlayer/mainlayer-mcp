/**
 * Mainlayer API client
 * Wraps the Mainlayer payment infrastructure REST API.
 */
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
export declare class MainlayerClient {
    private apiKey;
    constructor(config: MainlayerConfig);
    private request;
    discoverResources(params: {
        query?: string;
        type?: string;
        fee_model?: string;
        limit?: number;
    }): Promise<Resource[]>;
    getResourceInfo(resourceId: string): Promise<Resource>;
    payForResource(params: {
        resource_id: string;
        payer_wallet: string;
        coupon_code?: string;
    }): Promise<Payment>;
    checkAccess(params: {
        resource_id: string;
        payer_wallet: string;
    }): Promise<Entitlement>;
    createResource(params: {
        slug: string;
        type: string;
        price_usdc: number;
        fee_model: string;
        description?: string;
        callback_url?: string;
        credits_per_payment?: number;
        duration_seconds?: number;
    }): Promise<Resource>;
    listMyResources(): Promise<Resource[]>;
    getAnalytics(params: {
        start_date?: string;
        end_date?: string;
    }): Promise<Analytics>;
    listPayments(): Promise<Payment[]>;
}
//# sourceMappingURL=mainlayer.d.ts.map