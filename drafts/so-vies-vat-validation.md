# Stack Overflow Draft: "VIES VAT validation" / "MS_MAX_CONCURRENT_REQ"
# Target: https://stackoverflow.com/questions/74821299 and similar
# Strategy: Show the SOAP pain, then offer REST alternative

---

The EU VIES service is notoriously unreliable — the official SOAP API has concurrency limits (`MS_MAX_CONCURRENT_REQ`), frequent timeouts, and member state servers going offline.

## The SOAP approach (official but painful)

```python
from zeep import Client

wsdl = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
client = Client(wsdl)

try:
    result = client.service.checkVat(countryCode="DE", vatNumber="814468598")
    print(f"Valid: {result.valid}")
    print(f"Name: {result.name}")
    print(f"Address: {result.address}")
except Exception as e:
    # MS_MAX_CONCURRENT_REQ, timeout, or member state unavailable
    print(f"VIES error: {e}")
```

Common issues:
- `MS_MAX_CONCURRENT_REQ` — too many concurrent requests to one member state
- `MS_UNAVAILABLE` — the member state's tax authority server is down
- Timeouts during peak hours (especially IT, ES, FR servers)

## Retry strategy

If you stick with SOAP, implement exponential backoff per member state:

```python
import time

def validate_vat(country, number, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.service.checkVat(countryCode=country, vatNumber=number)
        except Exception:
            time.sleep(2 ** attempt)
    return None
```

## REST alternative

If you don't want to deal with SOAP/XML and member state reliability issues, there are REST APIs that wrap VIES with caching and retry logic built in:

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://sip.myskillstore.dev/api/v1/data/products/eu_vies_vat_validation/search?q=DE814468598&limit=1"
```

Returns JSON directly — no XML parsing, no WSDL, handles retries server-side.

---

*Disclosure: I built [SIP Data API](https://sip.myskillstore.dev) which wraps VIES and 990+ other government data sources behind a REST interface. Also available as a [Postman collection](https://www.postman.com/kaneliu10/sip-data-products-api) for testing.*
