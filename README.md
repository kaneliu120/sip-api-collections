# SIP Data API — Postman Collections

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/kaneliu10/sip-data-products-api)

Access **990+ government data products across 42 countries** — company registries, sanctions lists, patents, building permits, healthcare databases, court decisions, procurement notices, and more. All data sourced from official government registries in real-time.

**87 example responses included** — see real API output without running a single request.

## Collections

### Government Data APIs (direct SIP API)

| Collection | Country | Products | Examples | Sectors |
|---|---|---|---|---|
| [US Government Data](postman/us-government-data.json) | 🇺🇸 United States | 175 | 6 | Business, Permits, Compliance, Health, Finance, Education, Transport |
| [Canada Government Data](postman/canada-government-data.json) | 🇨🇦 Canada | 89 | 12 | Business, Permits, Procurement, Health, Finance, Energy, Education, Legal |
| [EU Government Data](postman/eu-government-data.json) | 🇪🇺 European Union | 85 | 12 | Financial Registries, Health, Energy, Education, Legal, Procurement |
| [Taiwan Government Data](postman/taiwan-government-data.json) | 🇹🇼 Taiwan | 56 | 10 | Stock Market, FDA, CDC, Environment, Food Safety |
| [France Government Data](postman/france-government-data.json) | 🇫🇷 France | 36 | 10 | Business, Construction, Health, Legal, Procurement |
| [UK Government Data](postman/uk-government-data.json) | 🇬🇧 United Kingdom | 31 | 7 | Charities, Planning, NHS, Case Law, Procurement |
| [Australia Government Data](postman/australia-government-data.json) | 🇦🇺 Australia | 28 | 9 | ASIC, Permits, Medicare, IP, Procurement |
| [Global Sanctions & Company Verification](postman/global-sanctions-company-verification.json) | 🌍 Global | 15 | 9 | OFAC, EU/CA Sanctions, GLEIF, VAT, FINRA, FDIC |

### Web Scraper Actors (Apify API)

| Collection | Actors | Examples |
|---|---|---|
| [SIP Web Scrapers](postman/sip-web-scrapers-apify.json) | Google Maps, YouTube, TikTok, LinkedIn Jobs, Reddit, Facebook Ads, Booking/Airbnb, eBay/Target, Zillow/Zumper, Stealth Scraper | 12 |

## Quick Start

### Option 1: Postman (recommended)

1. Visit the [SIP Data Products API workspace](https://www.postman.com/kaneliu10/sip-data-products-api)
2. Fork the collection you need
3. Set your `api_key` variable
4. Send your first request

### Option 2: Import from this repo

1. Download any `.json` file from the `postman/` directory
2. In Postman, click **Import** and select the file
3. Set the `api_key` variable in collection settings

### Option 3: cURL

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/us_ofac_sanctions/search?q=Rosneft&limit=10"
```

## Authentication

All SIP API endpoints require an `X-API-Key` header. Get your key at [sip.myskillstore.dev](https://sip.myskillstore.dev).

For Apify Actor collections, use a Bearer token from [Apify Console](https://console.apify.com/account/integrations).

## Related Resources

- **Postman Workspace**: [SIP Data Products API](https://www.postman.com/kaneliu10/sip-data-products-api)
- **Apify Store**: [lentic_clockss](https://apify.com/lentic_clockss) (43 Actors)
- **API Documentation**: [sip.myskillstore.dev/docs](https://sip.myskillstore.dev/docs)
- **Support**: admin@myskillstore.dev

## License

MIT
