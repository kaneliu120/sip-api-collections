"""
Screen an entity against 4 government sanctions lists in one API call.

Covers:
  - OFAC SDN (US Treasury) — ~9,000 sanctioned individuals, entities, vessels
  - EU Financial Sanctions — all EU restrictive measures
  - Canada Autonomous Sanctions — ~5,500 entries
  - AU ASIC Banned Persons — disqualified from financial services

Usage:
  pip install httpx
  export SIP_API_KEY="your_key_here"
  python sanctions-screening.py "Rosneft"

Get your API key: https://sip.myskillstore.dev
Postman Collection: https://www.postman.com/kaneliu10/sip-data-products-api
"""

import httpx
import os
import sys

API_KEY = os.environ.get("SIP_API_KEY", "")
BASE = "https://sip.myskillstore.dev/api/v1/data"

SANCTIONS_SOURCES = [
    ("us_ofac_sanctions", "OFAC SDN (US)"),
    ("eu_sanctions_consolidated_list", "EU Financial Sanctions"),
    ("ca_sanctions_consolidated", "Canada Sanctions"),
    ("au_asic_banned_disqualified_persons", "AU ASIC Banned Persons"),
]


def screen_entity(name: str) -> dict:
    """Screen a name against all sanctions lists. Returns hits per source."""
    results = {}
    headers = {"X-API-Key": API_KEY}

    with httpx.Client(timeout=30) as client:
        for product_id, label in SANCTIONS_SOURCES:
            resp = client.get(
                f"{BASE}/products/{product_id}/search",
                params={"q": name, "limit": 10},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            hits = data.get("results", [])
            results[label] = hits
            status = f"{len(hits)} hit(s)" if hits else "CLEAR"
            print(f"  [{label}] {status}")

    return results


if __name__ == "__main__":
    if not API_KEY:
        print("Set SIP_API_KEY environment variable first.")
        print("Get your key at: https://sip.myskillstore.dev")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "Rosneft"
    print(f"\nScreening: {query}\n")

    results = screen_entity(query)

    total_hits = sum(len(v) for v in results.values())
    print(f"\nTotal: {total_hits} hit(s) across {len(SANCTIONS_SOURCES)} lists")

    if total_hits > 0:
        print("\n--- Sample matches ---")
        for source, hits in results.items():
            for hit in hits[:2]:
                name = hit.get("name") or hit.get("entity_name") or "N/A"
                etype = hit.get("entity_type", "")
                print(f"  {source}: {name} ({etype})")
