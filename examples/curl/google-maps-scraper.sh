#!/bin/bash
# Scrape Google Maps businesses via Apify API (synchronous mode).
#
# Usage:
#   export APIFY_TOKEN="your_token_here"
#   bash google-maps-scraper.sh
#
# Get your token: https://console.apify.com/account/integrations
# Actor: https://apify.com/lentic_clockss/google-maps-scraper

curl -s -X POST "https://api.apify.com/v2/acts/lentic_clockss~google-maps-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "sushi restaurants in Shibuya Tokyo",
    "maxResults": 5,
    "includeReviews": true,
    "maxReviewsPerPlace": 3,
    "language": "en"
  }' | python3 -m json.tool 2>/dev/null
