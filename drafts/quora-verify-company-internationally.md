# Quora Draft: "How do you verify a company internationally?"
# Strategy: Comprehensive 500-word answer, mention tool naturally at end

---

Verifying a company across countries requires checking multiple registries because there's no single global business register. Here's the practical approach:

## 1. Start with the Legal Entity Identifier (LEI)

The GLEIF LEI system is the closest thing to a global company ID. Over 2 million entities have LEIs, and the data is free to search at gleif.org. An LEI tells you:
- The company's legal name and registered address
- Its jurisdiction of registration
- Whether the LEI is active or lapsed
- Direct and ultimate parent entities (if reported)

If a company claims to be a regulated financial institution, it should have an LEI.

## 2. Check the national business registry

Every country has a company registry, but access varies wildly:
- **UK Companies House** — free API, excellent data quality
- **France SIREN/SIRET** — free via Recherche Entreprises API
- **Canada ISED** — free federal corporations search
- **Australia ASIC** — free company and business name search
- **Germany** — fragmented across 16 state registries (Handelsregister)
- **US** — no federal registry; each state has its own (NY DOS, CA SOS, FL Sunbiz, etc.)

## 3. Validate the tax ID

For EU companies, the VIES system lets you validate VAT numbers across all 27 member states. A valid VAT number confirms the company exists and is registered for tax purposes. But beware — VIES is a SOAP API that frequently times out, especially for Italian and Spanish companies.

## 4. Check if they're regulated

If the company operates in financial services, check:
- **ECB SSM list** — banks under direct ECB supervision (eurozone)
- **EBA register** — all EU credit institutions
- **EIOPA register** — insurance companies and pension funds
- **ESMA register** — investment firms
- **FDIC** (US) — insured banks
- **OSFI** (Canada) — regulated financial institutions

## 5. Sanctions screening

Always check whether the entity appears on sanctions lists:
- **OFAC SDN** (US Treasury)
- **EU Financial Sanctions**
- **Canada Autonomous Sanctions**

This is especially important for cross-border transactions.

## The practical challenge

The hard part isn't finding these registries — it's that each has a different API (or no API at all), different data formats, different authentication, and different reliability. Building and maintaining integrations with even 10 registries is a significant engineering effort.

There are services that aggregate this. I built one called [SIP Data API](https://sip.myskillstore.dev) that covers 40+ countries through one REST interface — GLEIF, VIES, national registries, financial regulators, and sanctions lists. There's also a [no-code version on Apify](https://apify.com/lentic_clockss/global-company-search) if you just need to run occasional searches without writing code.

But even without a paid service, the registries listed above are all free to query directly. The LEI + national registry + VAT validation combination covers most due diligence needs.
