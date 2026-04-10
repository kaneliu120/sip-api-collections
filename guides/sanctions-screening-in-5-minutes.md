# Sanctions Screening in 5 Minutes

Screen any entity against US, EU, Canada, and Australia sanctions lists using a single REST API. No SOAP, no XML parsing, no multiple registrations — one API key, four jurisdictions.

## The Problem

If you need to check whether a company or individual appears on government sanctions lists, you typically face:

- **OFAC** (US): Bulk CSV download or undocumented search, no official REST API
- **EU Financial Sanctions**: 24MB XML file, updated irregularly, requires XML parsing
- **Canada**: PDF-based list with no machine-readable search
- **Australia ASIC**: Separate CKAN portal with different query syntax

Each source has different data formats, update frequencies, and access methods. Building and maintaining integrations with all four takes weeks of development time.

## The Solution

The SIP API normalizes all four sources behind one REST endpoint:

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/us_ofac_sanctions/search?q=Rosneft&limit=10"
```

Response:

```json
{
  "results": [
    {
      "name": "AKADEMIK GUBKIN",
      "entity_type": "vessel",
      "program": "UKRAINE-EO13662] [RUSSIA-EO14024",
      "vessel_type": "Crude Oil Tanker",
      "vessel_flag": "Russia",
      "entity_id": "51856",
      "list_source": "OFAC_SDN"
    }
  ],
  "meta": { "total": 12, "limit": 10, "query": "Rosneft" }
}
```

## Step-by-Step

### 1. Get an API Key

Sign up at [sip.myskillstore.dev](https://sip.myskillstore.dev) and generate a key.

### 2. Screen Against All Four Lists

**Python:**

```python
import httpx

API_KEY = "your_key"
BASE = "https://sip.myskillstore.dev/api/v1/data"

sources = [
    "us_ofac_sanctions",
    "eu_sanctions_consolidated_list",
    "ca_sanctions_consolidated",
    "au_asic_banned_disqualified_persons",
]

for source in sources:
    resp = httpx.get(
        f"{BASE}/products/{source}/search",
        params={"q": "Gazprom", "limit": 5},
        headers={"X-API-Key": API_KEY},
    )
    hits = resp.json().get("results", [])
    print(f"{source}: {len(hits)} hits")
```

**cURL:**

```bash
for source in us_ofac_sanctions eu_sanctions_consolidated_list ca_sanctions_consolidated; do
  echo "--- $source ---"
  curl -s -H "X-API-Key: YOUR_KEY" \
    "https://sip.myskillstore.dev/api/v1/data/products/$source/search?q=Gazprom&limit=5"
done
```

### 3. Export for Compliance Records

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/us_ofac_sanctions/export?format=csv&q=Russia&limit=1000" \
  -o ofac_russia_matches.csv
```

## Available Sanctions Data

| Source | Product ID | Coverage | Records |
|---|---|---|---|
| OFAC SDN (US) | `us_ofac_sanctions` | Individuals, entities, vessels, aircraft | ~9,000 |
| EU Financial Sanctions | `eu_sanctions_consolidated_list` | All EU restrictive measures | ~2,000 |
| Canada Sanctions | `ca_sanctions_consolidated` | Autonomous sanctions (non-UN) | ~5,500 |
| AU ASIC Banned Persons | `au_asic_banned_disqualified_persons` | Financial services bans | Varies |
| ESMA Enforcement | `eu_esma_sanctions` | Securities market enforcement | ~1,400 |
| FINRA BrokerCheck | `us_finance_finra_brokercheck` | US broker-dealer records | Varies |
| FDIC Bank Failures | `us_fdic_failures` | Failed US banks | ~3,600 |

## No-Code Alternative

Don't want to write code? Use the [Apify Actor](https://apify.com/lentic_clockss/global-sanctions-screening) — enter a name, click Start, get results.

## Try It Now

- **Postman**: [Fork the collection](https://www.postman.com/kaneliu10/sip-data-products-api) — 9 pre-built requests with example responses
- **Python**: [sanctions-screening.py](../examples/python/sanctions-screening.py)
- **cURL**: [sanctions-screening.sh](../examples/curl/sanctions-screening.sh)

---

*This guide is part of the [SIP Data API](https://github.com/kaneliu120/sip-api-collections) collection. 990+ government data products across 42 countries.*
