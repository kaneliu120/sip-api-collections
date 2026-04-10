#!/bin/bash
# Screen an entity against OFAC, EU, Canada, and AU sanctions lists.
#
# Usage:
#   export SIP_API_KEY="your_key_here"
#   bash sanctions-screening.sh "Rosneft"
#
# Get your API key: https://sip.myskillstore.dev

QUERY="${1:-Rosneft}"
BASE="https://sip.myskillstore.dev/api/v1/data"

echo "Screening: $QUERY"
echo "========================================"

for source in us_ofac_sanctions eu_sanctions_consolidated_list ca_sanctions_consolidated au_asic_banned_disqualified_persons; do
  echo ""
  echo "--- $source ---"
  curl -s -H "X-API-Key: $SIP_API_KEY" \
    "$BASE/products/$source/search?q=$(echo $QUERY | sed 's/ /+/g')&limit=5" | \
    python3 -m json.tool 2>/dev/null || echo "(requires python3 for formatting)"
done
