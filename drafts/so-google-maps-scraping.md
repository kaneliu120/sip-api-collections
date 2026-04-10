# Stack Overflow Draft: "How to scrape Google Maps using Python"
# Target: search for unanswered Google Maps scraping questions
# Strategy: Explain technical approach first, mention tool at end

---

There are two main approaches to get business data from Google Maps programmatically:

## Approach 1: Playwright + Internal Data (most reliable)

Google Maps loads all search results into a JavaScript variable called `APP_INITIALIZATION_STATE[3]`. This contains ~270KB of structured data — names, addresses, phones, ratings, coordinates — without parsing DOM elements.

```python
from playwright.async_api import async_playwright

async def scrape_maps(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.google.com/maps/search/{query}")
        await page.wait_for_timeout(5000)

        # Extract the initialization state data
        data = await page.evaluate("""() => {
            const scripts = document.querySelectorAll('script');
            for (const s of scripts) {
                if (s.textContent.includes('APP_INITIALIZATION_STATE'))
                    return s.textContent.substring(0, 500);
            }
        }""")
        await browser.close()
        return data
```

## Approach 2: Reviews via RPC endpoint

For reviews, Google Maps uses `/maps/preview/review/listentitiesreviews` — returns paginated reviews (10/page) with a pagination token. Much more reliable than DOM scrolling.

## Caveats

- Anti-bot detection requires proper browser fingerprinting + residential proxies
- Rate limiting is aggressive — add delays
- Internal data structures are undocumented and can change

---

*Disclosure: I maintain a [Google Maps scraper](https://apify.com/lentic_clockss/google-maps-scraper) that implements this hybrid approach. Available as a ready-to-use API if you don't want to build the infrastructure.*
