"""
Scrape Google Maps businesses via Apify Actor.

Returns business name, address, phone, website, rating, reviews,
opening hours, and GPS coordinates.

Usage:
  pip install apify-client
  export APIFY_TOKEN="your_token_here"
  python google-maps-scraper.py "sushi restaurants in Tokyo"

Get your token: https://console.apify.com/account/integrations
Actor page: https://apify.com/lentic_clockss/google-maps-scraper
"""

from apify_client import ApifyClient
import os
import sys

TOKEN = os.environ.get("APIFY_TOKEN", "")


def scrape_google_maps(query: str, max_results: int = 10, include_reviews: bool = True):
    client = ApifyClient(TOKEN)

    run_input = {
        "searchQuery": query,
        "maxResults": max_results,
        "includeReviews": include_reviews,
        "maxReviewsPerPlace": 5,
        "language": "en",
    }

    print(f"Running Google Maps Scraper...")
    run = client.actor("lentic_clockss/google-maps-scraper").call(run_input=run_input)

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"Found {len(items)} businesses\n")

    for i, item in enumerate(items, 1):
        print(f"{i}. {item.get('name', 'N/A')}")
        print(f"   Address: {item.get('address', 'N/A')}")
        print(f"   Phone: {item.get('phone', 'N/A')}")
        print(f"   Rating: {item.get('rating', 'N/A')} ({item.get('reviews_count', 0)} reviews)")
        print(f"   Website: {item.get('website', 'N/A')}")

        reviews = item.get("reviews", [])
        if reviews:
            print(f"   Top review: \"{reviews[0].get('text', '')[:100]}...\"")
        print()

    return items


if __name__ == "__main__":
    if not TOKEN:
        print("Set APIFY_TOKEN environment variable first.")
        print("Get your token at: https://console.apify.com/account/integrations")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "sushi restaurants in Shibuya Tokyo"
    scrape_google_maps(query)
