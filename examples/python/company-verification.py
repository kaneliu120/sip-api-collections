"""
Verify a company across GLEIF LEI, EU VAT (VIES), and ECB supervised banks.

Three checks in one script:
  1. GLEIF LEI lookup — globally unique legal entity identifier
  2. EU VAT validation — verify VAT number across 27 EU countries
  3. ECB supervised banks — check if entity is under ECB supervision

Usage:
  pip install httpx
  export SIP_API_KEY="your_key_here"
  python company-verification.py "Deutsche Bank"

Get your API key: https://sip.myskillstore.dev
Postman Collection: https://www.postman.com/kaneliu10/sip-data-products-api
"""

import httpx
import os
import sys

API_KEY = os.environ.get("SIP_API_KEY", "")
BASE = "https://sip.myskillstore.dev/api/v1/data"


def search_product(client: httpx.Client, product_id: str, query: str, limit: int = 5):
    resp = client.get(
        f"{BASE}/products/{product_id}/search",
        params={"q": query, "limit": limit},
        headers={"X-API-Key": API_KEY},
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def verify_company(name: str):
    with httpx.Client(timeout=30) as client:
        # 1. GLEIF LEI
        print("1. GLEIF LEI Registry")
        lei_results = search_product(client, "us_gleif_lei", name)
        if lei_results:
            r = lei_results[0]
            print(f"   Found: {r.get('legal_name', name)}")
            print(f"   LEI: {r.get('lei', 'N/A')}")
            print(f"   Jurisdiction: {r.get('jurisdiction', 'N/A')}")
            print(f"   Status: {r.get('status', 'N/A')}")
        else:
            print("   No LEI record found")

        # 2. ECB Supervised Banks
        print("\n2. ECB Supervised Banks (SSM)")
        ecb_results = search_product(client, "eu_ecb_supervised_banks", name)
        if ecb_results:
            r = ecb_results[0]
            print(f"   Found: {r.get('entity_name', name)}")
            print(f"   Country: {r.get('country', 'N/A')}")
            print(f"   Supervised: YES (significant institution)")
        else:
            print("   Not under direct ECB supervision")

        # 3. EU VAT (only if VAT number is provided)
        print("\n3. EU VAT Validation (VIES)")
        print("   Provide a VAT number (e.g. DE814468598) to validate.")
        print("   Example: python company-verification.py DE814468598")

        # Check if the query looks like a VAT number
        if len(name) >= 4 and name[:2].isalpha() and any(c.isdigit() for c in name):
            vat_results = search_product(client, "eu_vies_vat_validation", name, limit=1)
            if vat_results:
                r = vat_results[0]
                valid = r.get("valid", False)
                company = r.get("company_name", "N/A")
                print(f"   VAT {name}: {'VALID' if valid else 'INVALID'}")
                print(f"   Registered to: {company}")
            else:
                print(f"   VAT {name}: No result")


if __name__ == "__main__":
    if not API_KEY:
        print("Set SIP_API_KEY environment variable first.")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "Deutsche Bank"
    print(f"\nVerifying: {query}\n{'='*40}\n")
    verify_company(query)
