"""
Search SEC EDGAR public company filings via SIP API.

Find 10-K annual reports, 10-Q quarterly filings, and 8-K current reports
by company name, ticker, or CIK number.

Usage:
  pip install httpx
  export SIP_API_KEY="your_key_here"
  python sec-edgar-search.py "Tesla"

Get your API key: https://sip.myskillstore.dev
Postman Collection: https://www.postman.com/kaneliu10/sip-data-products-api
"""

import httpx
import os
import sys

API_KEY = os.environ.get("SIP_API_KEY", "")
BASE = "https://sip.myskillstore.dev/api/v1/data"


def search_edgar(query: str, limit: int = 10):
    headers = {"X-API-Key": API_KEY}

    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{BASE}/products/us_sec_edgar/search",
            params={"q": query, "limit": limit},
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

    results = data.get("results", [])
    meta = data.get("meta", {})

    print(f"Found {meta.get('total', len(results))} filings\n")

    for r in results:
        company = r.get("company_name", "N/A")
        ticker = r.get("ticker", "")
        filing = r.get("filing_type", "")
        date = r.get("filed_date", "")
        cik = r.get("cik", "")
        ticker_display = f" ({ticker})" if ticker else ""
        print(f"  {company}{ticker_display}")
        print(f"    Filing: {filing} | Date: {date} | CIK: {cik}")
        print()

    return results


if __name__ == "__main__":
    if not API_KEY:
        print("Set SIP_API_KEY environment variable first.")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "Tesla"
    print(f"\nSearching SEC EDGAR: {query}\n{'='*40}\n")
    search_edgar(query)
