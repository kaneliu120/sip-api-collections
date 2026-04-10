#!/bin/bash
# Verify a company via GLEIF LEI + ECB supervised banks + EU VAT.
#
# Usage:
#   export SIP_API_KEY="your_key_here"
#   bash company-verification.sh "Deutsche Bank"
#   bash company-verification.sh "DE814468598"   # VAT validation
#
# Get your API key: https://sip.myskillstore.dev

QUERY="${1:-Deutsche Bank}"
BASE="https://sip.myskillstore.dev/api/v1/data"
HEADER="X-API-Key: $SIP_API_KEY"

echo "Verifying: $QUERY"
echo "========================================"

echo ""
echo "1. GLEIF LEI Registry"
curl -s -H "$HEADER" "$BASE/products/us_gleif_lei/search?q=$(echo $QUERY | sed 's/ /+/g')&limit=3" | python3 -m json.tool 2>/dev/null

echo ""
echo "2. ECB Supervised Banks"
curl -s -H "$HEADER" "$BASE/products/eu_ecb_supervised_banks/search?q=$(echo $QUERY | sed 's/ /+/g')&limit=3" | python3 -m json.tool 2>/dev/null

echo ""
echo "3. EU VAT Validation (VIES)"
curl -s -H "$HEADER" "$BASE/products/eu_vies_vat_validation/search?q=$(echo $QUERY | sed 's/ /+/g')&limit=1" | python3 -m json.tool 2>/dev/null
