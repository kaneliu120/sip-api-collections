# Stack Overflow Draft: "How to get data from SEC EDGAR Python"
# Target: https://stackoverflow.com/questions/73862886
# Strategy: Show modern full-text search approach

---

SEC EDGAR now has a full-text search API that's much easier than parsing XBRL or bulk downloads.

## Modern approach: EDGAR Full-Text Search

```python
import httpx

# EDGAR full-text search (no API key needed, but respect rate limits)
resp = httpx.get(
    "https://efts.sec.gov/LATEST/search-index",
    params={
        "q": '"Tesla" AND "10-K"',
        "dateRange": "custom",
        "startdt": "2024-01-01",
        "enddt": "2025-12-31",
    },
    headers={"User-Agent": "YourName your@email.com"},
)
data = resp.json()

for hit in data.get("hits", {}).get("hits", []):
    source = hit["_source"]
    print(f"{source['entity_name']} | {source['form_type']} | {source['file_date']}")
```

## Key points

- Always set a `User-Agent` header with your name and email — SEC blocks requests without it
- Rate limit: max 10 requests/second
- The full-text search index covers all filing types (10-K, 10-Q, 8-K, etc.)
- For structured financial data (revenue, assets), you need the XBRL companyfacts endpoint:

```python
# Get all financial facts for a company by CIK
resp = httpx.get(
    "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json",
    headers={"User-Agent": "YourName your@email.com"},
)
facts = resp.json()
# Navigate: facts["facts"]["us-gaap"]["Revenue"]["units"]["USD"]
```

---

*Disclosure: I also offer a [REST API](https://sip.myskillstore.dev) that wraps EDGAR and 990+ other government data sources with unified search, pagination, and export. [Postman collection](https://www.postman.com/kaneliu10/sip-data-products-api) available for testing.*
