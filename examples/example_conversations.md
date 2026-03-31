# Example Conversations with Claude Desktop

These examples show what you can say to Claude after configuring the Mainlayer MCP server.

---

## Getting Started: Register as a Vendor

**You:** Register me as a vendor on Mainlayer. My service is called "AI Data Insights" and my website is https://aidatainsights.example.com.

**Claude:** I'll register you as a vendor on Mainlayer right now.

_[calls create_vendor]_

Done! Your vendor profile has been created with ID `vendor_abc123`. You're now ready to list paid resources that other agents and users can purchase.

---

## Create a Paid Resource

**You:** Create a new paid API called "Real-Time Stock Sentiment" that charges $0.02 per call. The endpoint is https://api.aidatainsights.example.com/sentiment.

**Claude:** I'll create that resource on Mainlayer now.

_[calls create_resource]_

Your resource has been created:
- **ID:** `res_xyz789`
- **Slug:** `real-time-stock-sentiment`
- **Price:** $0.02 per call
- **Fee model:** pay_per_call
- **Status:** active

Other agents can now discover and pay to use your sentiment API.

---

## Add a Pricing Plan

**You:** Add a "Pro" pricing plan to my stock sentiment API at $0.05 per call with 50 credits per payment.

**Claude:** I'll add that Pro plan now.

_[calls create_plan with resource_id="res_xyz789", name="Pro", fee_model="pay_per_call", price_usdc=0.05, credits_per_payment=50]_

Pro plan created with ID `plan_pro_001`. Buyers can now choose between the Basic ($0.02) and Pro ($0.05) tiers.

---

## Check Your Earnings

**You:** How much have I earned on Mainlayer this month?

**Claude:** Let me pull up your earnings analytics.

_[calls get_earnings with start_date="2026-03-01", end_date="2026-03-31"]_

Here's your March 2026 performance:
- **Total revenue:** $342.58
- **Payment count:** 17,129 calls
- **Active subscribers:** 8

Your top resource is `real-time-stock-sentiment` with $289.40 in revenue.

---

## List Your Resources

**You:** Show me all the resources I have listed on Mainlayer.

**Claude:** I'll fetch your resources now.

_[calls list_resources]_

You have 3 active resources:
1. `real-time-stock-sentiment` — $0.02/call (pay_per_call)
2. `earnings-report-api` — $9.99/month (subscription)
3. `historical-data-pack` — $49.00 (one_time)

---

## Discover Paid Resources (as a buyer)

**You:** Find me a weather API I can pay for.

**Claude:** I'll search the Mainlayer marketplace for weather APIs.

_[calls discover_resources with query="weather"]_

I found 3 weather APIs:
1. **OpenWeather Pro** — $0.01/call (`res_weather_001`)
2. **Global Forecast API** — $4.99/month (`res_weather_002`)
3. **Historical Climate Data** — $19.99 one-time (`res_weather_003`)

Which one would you like to use? I can check if you already have access and pay for it if needed.

---

## Check Access Before Paying

**You:** Check if my wallet 0xMyWallet already has access to res_weather_001.

**Claude:** Let me check your access.

_[calls check_access with resource_id="res_weather_001", payer_wallet="0xMyWallet"]_

You don't currently have access to this resource. Would you like me to pay for it? It's $0.01 per call.

---

## Pay for a Resource

**You:** Yes, go ahead and pay for res_weather_001 using wallet 0xMyWallet.

**Claude:** Processing payment now.

_[calls pay_for_resource with resource_id="res_weather_001", payer_wallet="0xMyWallet"]_

Payment successful!
- **Transaction ID:** `pay_abc123`
- **Amount:** $0.01
- **Credits granted:** 100 API calls
- **Status:** confirmed

You now have access to the OpenWeather Pro API.

---

## Set Up a Subscription

**You:** Subscribe my wallet 0xMyWallet to the earnings-report-api monthly plan.

**Claude:** I'll set up that subscription now.

_[calls create_subscription with resource_id="res_earnings_002", payer_wallet="0xMyWallet"]_

Subscription active!
- **Subscription ID:** `sub_xyz456`
- **Next billing date:** April 30, 2026
- **Status:** active

You now have automatic monthly access to the Earnings Report API.
