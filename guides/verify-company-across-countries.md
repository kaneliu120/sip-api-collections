# Verify a Company Across Countries

Look up company registration data, legal entity identifiers, VAT status, and regulatory standing across 40+ countries through one API.

## The Problem

Know-Your-Business (KYB) verification typically requires checking multiple registries:

- **GLEIF** for LEI (Legal Entity Identifier)
- **EU VIES** for VAT validation
- **National registries** for incorporation status (Companies House, ISED, ASIC, etc.)
- **Financial regulators** for supervised entity status (ECB, EBA, EIOPA, ESMA)

Each has different APIs, authentication, and data formats. Some have no API at all.

## The Solution

The SIP API provides a unified search interface across 80+ company data sources in 40+ countries:

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/us_gleif_lei/search?q=Apple%20Inc&limit=5"
```

## Common Verification Workflows

### Workflow 1: Full Company Due Diligence

```python
import httpx

API_KEY = "your_key"
BASE = "https://sip.myskillstore.dev/api/v1/data"
headers = {"X-API-Key": API_KEY}

def verify(name):
    checks = {
        "GLEIF LEI": "us_gleif_lei",
        "ECB Supervised": "eu_ecb_supervised_banks",
        "OFAC Sanctions": "us_ofac_sanctions",
        "EU Sanctions": "eu_sanctions_consolidated_list",
    }

    with httpx.Client(timeout=30) as client:
        for label, product_id in checks.items():
            resp = client.get(
                f"{BASE}/products/{product_id}/search",
                params={"q": name, "limit": 3},
                headers=headers,
            )
            hits = resp.json().get("results", [])
            status = f"{len(hits)} match(es)" if hits else "CLEAR"
            print(f"  [{label}] {status}")

verify("Deutsche Bank")
```

### Workflow 2: EU VAT Validation

Validate a VAT number and get the registered company name and address:

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/eu_vies_vat_validation/search?q=DE814468598&limit=1"
```

### Workflow 3: Country-Specific Company Search

Search the national business registry for a specific country:

| Country | Product ID | Records |
|---|---|---|
| 🇺🇸 US (9 states) | `us_business_ny`, `us_business_ca`, etc. | 10M+ |
| 🇨🇦 Canada Federal | `ca_federal_corporations` | 1.55M |
| 🇨🇦 BC (OrgBook) | `ca_orgbook_bc_entity` | 2.5M |
| 🇦🇺 Australia | `au_asic_companies` | ASIC registry |
| 🇫🇷 France | `fr_recherche_entreprises_business` | SIREN/SIRET |
| 🇹🇼 Taiwan | `tw_twse_listed_companies` | 1,070 listed |
| 🇬🇧 UK | `uk_charity_commission_register` | Charities |
| 🇮🇱 Israel | `il_ica_companies_search` | ICA registry |
| 🌍 Global GLEIF | `us_gleif_lei` + 20+ country variants | 2M+ LEIs |

### Workflow 4: Financial Institution Check

Verify if an entity is a regulated financial institution:

```python
financial_checks = [
    ("eu_ecb_supervised_banks", "ECB Supervised Banks"),
    ("eu_eba_credit_institutions", "EBA Credit Institutions"),
    ("eu_eiopa_insurance_register", "EIOPA Insurance"),
    ("eu_esma_investment_firms", "ESMA Investment Firms"),
    ("us_fdic_institutions", "US FDIC Insured Banks"),
    ("ca_osfi_regulated_fi", "Canada OSFI Regulated"),
]
```

## No-Code Alternative

Use the [Global Company Search Actor](https://apify.com/lentic_clockss/global-company-search) on Apify — searches 82 data sources across 40+ countries in one run, no code needed.

## Try It Now

- **Postman**: [Fork the collection](https://www.postman.com/kaneliu10/sip-data-products-api) — pre-built requests for GLEIF, VIES, ECB, and more
- **Python**: [company-verification.py](../examples/python/company-verification.py)
- **cURL**: [company-verification.sh](../examples/curl/company-verification.sh)

---

*This guide is part of the [SIP Data API](https://github.com/kaneliu120/sip-api-collections) collection. 990+ government data products across 42 countries.*
