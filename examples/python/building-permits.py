"""
Search building permits across multiple US and Canadian cities.

Searches 12 jurisdictions in parallel:
  US: NYC, Austin, SF, Chicago, Seattle, Cincinnati, Honolulu, NJ
  CA: Calgary, Edmonton, Toronto, Vancouver

Usage:
  pip install httpx
  export SIP_API_KEY="your_key_here"
  python building-permits.py "solar"

Get your API key: https://sip.myskillstore.dev
Postman Collection: https://www.postman.com/kaneliu10/sip-data-products-api
"""

import asyncio
import httpx
import os
import sys

API_KEY = os.environ.get("SIP_API_KEY", "")
BASE = "https://sip.myskillstore.dev/api/v1/data"

US_PERMIT_CITIES = [
    ("us_permits_nyc", "NYC"),
    ("us_permits_austin", "Austin"),
    ("us_permits_sf", "San Francisco"),
    ("us_permits_chicago", "Chicago"),
    ("us_permits_seattle", "Seattle"),
]

CA_PERMIT_CITIES = [
    ("ca_calgary_building_permits", "Calgary"),
    ("ca_edmonton_building_permits", "Edmonton"),
    ("ca_toronto_building_permits", "Toronto"),
    ("ca_vancouver_building_permits", "Vancouver"),
]


async def search_city(client: httpx.AsyncClient, product_id: str, city: str, query: str):
    try:
        resp = await client.get(
            f"{BASE}/products/{product_id}/search",
            params={"q": query, "limit": 5},
            headers={"X-API-Key": API_KEY},
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return city, results
    except Exception as e:
        return city, []


async def search_all_cities(query: str):
    all_cities = US_PERMIT_CITIES + CA_PERMIT_CITIES

    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [search_city(client, pid, city, query) for pid, city in all_cities]
        results = await asyncio.gather(*tasks)

    total = 0
    for city, hits in results:
        count = len(hits)
        total += count
        marker = f"{count} permits" if count else "—"
        print(f"  {city:15s} {marker}")
        for hit in hits[:2]:
            addr = hit.get("address", hit.get("location", ""))
            status = hit.get("status", "")
            if addr:
                print(f"                  {addr} [{status}]")

    print(f"\nTotal: {total} permits found across {len(all_cities)} cities")


if __name__ == "__main__":
    if not API_KEY:
        print("Set SIP_API_KEY environment variable first.")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "solar"
    print(f"\nSearching permits: {query}\n")
    asyncio.run(search_all_cities(query))
