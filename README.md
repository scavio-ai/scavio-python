# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) Search API. Access real-time data from 36 sources -- Google, Amazon, Walmart, Costco, Mercado Libre, eBay, Target, Home Depot, YouTube, Reddit, X, TikTok, TikTok Shop, Instagram, LinkedIn, Threads, Kuaishou, Zillow, Redfin, Realtor.com, Rightmove, Booking.com, Tripadvisor, Airbnb, Yelp, Indeed, Glassdoor, the Apple App Store, Google Play, SEC EDGAR, Companies House, G2, Capterra, Trustpilot, Google Ads Transparency and the Meta Ad Library -- plus `extract()` for reading any URL, all with a single API key. Built for AI agents, LLM applications, and data pipelines.

> One API key, 36 data sources, 233 endpoints, structured JSON with knowledge graphs. A powerful alternative to Tavily, SerpAPI, and ScraperAPI for developers who need more than just web search.

## Why Scavio

| Feature | Scavio | Tavily | SerpAPI | ScraperAPI |
|---------|--------|--------|---------|------------|
| Google Search | Yes | Yes | Yes | Yes |
| Amazon Products | Yes | No | Yes | No |
| Walmart Products | Yes | No | No | No |
| Costco Warehouse Prices, Stock, Gas and Coupons (13 endpoints) | Yes | No | No | No |
| Trustpilot Businesses and Reviews (6 endpoints) | Yes | No | No | No |
| Mercado Libre Listings, Reviews and Best Sellers (MX, BR, AR, CO; 5 endpoints) | Yes | No | No | No |
| YouTube Search | Yes | No | Yes | No |
| Reddit Data (12 endpoints) | Yes | No | No | No |
| X Data (11 endpoints) | Yes | No | No | No |
| TikTok Data (11 endpoints) | Yes | No | No | No |
| TikTok Shop Data (8 endpoints) | Yes | No | No | No |
| Instagram Data (12 endpoints) | Yes | No | No | No |
| LinkedIn Data (9 endpoints) | Yes | No | No | No |
| eBay Sold-Listing Price History | Yes | No | No | No |
| Real Estate (Zillow + Redfin + Realtor.com + Rightmove, 19 endpoints) | Yes | No | No | No |
| UK Sold House Prices since 1995 (Rightmove, England and Wales) | Yes | No | No | No |
| Travel (Booking + Airbnb + Tripadvisor, 10 endpoints) | Yes | No | No | No |
| Jobs & Employers (Indeed + Glassdoor, 8 endpoints) | Yes | No | No | No |
| Ad Transparency (Meta + Google, 6 endpoints) | Yes | No | No | No |
| Filings (SEC EDGAR + Companies House, 10 endpoints) | Yes | No | No | No |
| Read Any URL (`extract`) | Yes | Yes | No | Yes |
| Data Sources | 36 | 1 | 1 per plan | 1 |
| Structured JSON | Yes | Yes | Yes | Raw HTML |
| Knowledge Graphs | Yes | No | Yes | No |
| Async Client | Yes | Yes | No | No |
| Single API Key | Yes | Yes | No | No |
| Rate Limiting Built-in | Yes | No | No | No |
| Automatic Retries + Backoff | Yes | No | No | No |
| Fully Typed Parameters | Yes | No | No | No |
| Type Hints (PEP 561) | Yes | Yes | No | No |

Tavily focuses on AI-optimized web search. SerpAPI offers SERP parsing across search engines with separate plans. ScraperAPI provides raw web scraping with proxy rotation. Scavio combines multi-source structured data in a single [search API for AI agents](https://scavio.dev/search-api-for-ai-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) with one SDK and one API key.

## Installation

```bash
pip install scavio
```

## Quick Start

Get your free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

```python
from scavio import ScavioClient

client = ScavioClient(api_key="sk_...")  # or set SCAVIO_API_KEY env var

results = client.search("best noise cancelling headphones 2026")
for r in results["organic_results"]:
    print(r["title"], r["link"])
```

Every method returns the API response as a plain `dict`. Amazon responses are
normalized to a stable, documented shape; the other endpoints keep each
platform's own field names, so fields vary by endpoint.

## Fully typed parameters

Every endpoint exposes all of its parameters as explicit, documented,
autocomplete-friendly keyword arguments with `Literal` types for enums. Your
editor shows the full parameter set, allowed enum values, and defaults inline.

```python
# Google web search with the full parameter surface
results = client.google.search(
    "electric cars",
    gl="us",                 # country of the search
    hl="en",                 # UI language
    location="Austin, Texas, United States",
    time_period="last_month",
    device="mobile",
)

# YouTube filters. The digit-named API fields (4k, 360, 3d) are exposed as
# valid Python identifiers: four_k, video_360, video_3d.
client.youtube.search("drone footage", four_k=True, hdr=True, duration="long")

# Amazon product lookup: pass the ASIN (sent to the API as `query`).
# `country` is the marketplace, as an ISO 3166-1 alpha-2 code.
client.amazon.product("B09XS7JWHH", country="gb")
```

### Forward-compatible passthrough

Any parameter the API adds in the future can be passed via `**extra` and is sent
verbatim, so you never have to wait for an SDK release:

```python
client.google.search("openai", **{"some_new_param": "value"})
```

## Retries and resilience

The client automatically retries transient failures (HTTP 429 and 5xx, plus
network/timeout errors) with exponential backoff, jitter, and `Retry-After`
support. Configure or disable it with `max_retries`.



### 1. AI Web Research -- Feed Search Results to an LLM

```python
from scavio import ScavioClient

client = ScavioClient()

results = client.search("latest advances in quantum computing 2026")

context = "\n\n".join(
    f"[{r['title']}]({r['link']})\n{r.get('snippet', '')}"
    for r in results["organic_results"]
)

prompt = f"Based on these search results, summarize the latest advances:\n\n{context}"
# Pass `prompt` to your LLM of choice (OpenAI, Anthropic, etc.)
print(prompt[:500])
```

### 2. Price Comparison -- Amazon vs Walmart

```python
from scavio import ScavioClient

client = ScavioClient()

query = "sony wh-1000xm5"
amazon = client.amazon.search(query, country="us")
walmart = client.walmart.search(query)

print("Amazon:")
for p in amazon["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")

print("\nWalmart:")
for p in walmart["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")
```

### 3. Product Lookup by ASIN, plus every seller offer

```python
from scavio import ScavioClient

client = ScavioClient()

data = client.amazon.product("B0BS1PRC4L")["data"]

print(f"Brand:   {data['brand']}")
print(f"Title:   {data['title']}")
print(f"Rating:  {data['rating']} ({data['reviews_count']} reviews)")
print(f"Price:   {data['price']} {data['currency']}")

# Same ASIN, every seller: price, condition, and who holds the buy box.
offers = client.amazon.offers("B0BS1PRC4L")["data"]
print(f"{offers['total_offers']} offers")
for o in offers["offers"][:5]:
    tag = " (buy box)" if o["is_buy_box_winner"] else ""
    print(f"  {o['price']} {o['currency']} - {o['seller_name']} [{o['condition']}]{tag}")
```

### 4. SEO Competitor Analysis

```python
from scavio import ScavioClient

client = ScavioClient()

results = client.search("best project management software", gl="us")

for r in results["organic_results"]:
    print(f"{r['position']}. {r['title']}")
    print(f"   {r['link']}")
```

### 5. News Aggregation

```python
from scavio import ScavioClient

client = ScavioClient()

news = client.google.news("AI startups")

for article in news["news_results"][:5]:
    print(f"[{article['source']}] {article['title']}")
    print(f"  {article['link']}")
    print()
```

### 6. YouTube Content Discovery

```python
from scavio import ScavioClient

client = ScavioClient()

videos = client.youtube.search("python tutorial", sort_by="view_count")

for v in videos["data"]["results"][:5]:
    print(f"{v['title']} ({v['view_count']:,} views)")
    print(f"  {v['url']}")

# Full details for a specific video (metadata() is a deprecated alias of video())
video = client.youtube.video("dQw4w9WgXcQ")
print(f"\n{video['data']['title']}")
print(f"  {video['data']['view_count']:,} views")

# Transcript, related videos, comments, channel, and streams
transcript = client.youtube.transcript("dQw4w9WgXcQ", format="text")
related = client.youtube.related("dQw4w9WgXcQ")
comments = client.youtube.comments("dQw4w9WgXcQ")
channel_id = client.youtube.channel_resolve("@mkbhd")["data"]["channel_id"]
channel = client.youtube.channel(channel_id)
streams = client.youtube.streams("dQw4w9WgXcQ")
```

### 7. Reddit Market Research

```python
from scavio import ScavioClient

client = ScavioClient()

posts = client.reddit.search("best mechanical keyboard")

for post in posts["data"]["results"]:
    print(f"r/{post['subreddit']} - {post['title']}")
    print(f"  {post['url']}")
    print()

# Drill into a subreddit, a single post, or a redditor. reddit.post() takes a
# url or a post_id and returns the post alone -- comments are a separate call.
feed = client.reddit.subreddit_posts("MechanicalKeyboards", sort="TOP")
detail = client.reddit.post(post_id="t3_1v6ngaf")
comments = client.reddit.post_comments("t3_1v6ngaf", sort="TOP")
history = client.reddit.user_posts("spez")
popular = client.reddit.popular()
trending = client.reddit.trending()
```

### 8. TikTok Hashtag Analysis

```python
from scavio import ScavioClient

client = ScavioClient()

hashtag = client.tiktok.hashtag(hashtag_name="python")
info = hashtag["data"]["challengeInfo"]

print(f"#{info['challenge']['title']}")
print(f"  Views: {int(info['statsV2']['viewCount']):,}")
print(f"  Videos: {int(info['statsV2']['videoCount']):,}")
```

### 9. Instagram Profile and Posts

```python
from scavio import ScavioClient

client = ScavioClient()

profile = client.instagram.profile(username="instagram")
user = profile["data"]["user"]
print(f"@{user['username']} - {user['edge_followed_by']['count']:,} followers")

posts = client.instagram.user_posts(username="instagram", count=12)
reels = client.instagram.user_reels(username="instagram")
hashtags = client.instagram.search_hashtags("fashion")
```

### 10. X Search and Profiles

```python
from scavio import ScavioClient

client = ScavioClient()

tweets = client.x.search("AI agents", search_type="Latest")
for t in tweets["data"]["timeline"][:5]:
    print(f"@{t['screen_name']}: {t['text'][:80]}")

# Profile, a user's tweets, followers, and a single tweet's replies
profile = client.x.user("elonmusk")
timeline = client.x.user_tweets("elonmusk")
followers = client.x.user_followers("elonmusk")
replies = client.x.tweet_comments("1808168603721650364", rank="top")
trending = client.x.trending(country="UnitedStates")
```

### 11. LinkedIn People and Companies

```python
from scavio import ScavioClient

client = ScavioClient()

# Member profile (1 credit) and their recent posts (10 credits per page). A
# handle or a full LinkedIn URL works anywhere.
person = client.linkedin.person(username="williamhgates")
person_posts = client.linkedin.person_posts(url="https://www.linkedin.com/in/williamhgates/")

# Company profile and its recent posts
company = client.linkedin.company(company="microsoft")
company_posts = client.linkedin.company_posts(company="microsoft")

# Jobs: search, then pull full detail for one listing
job_results = client.linkedin.search_jobs("software engineer", location="United States")
job = client.linkedin.job(job_id=job_results["data"]["data"][0]["id"])

# A post and its comments (10 per page)
post = client.linkedin.post(post_id="7488618410256523265")
comments = client.linkedin.post_comments(post_id="7488618410256523265", page=1)
```

> **Retired endpoints.** The LinkedIn data behind `person_contact`,
> `company_people`, `company_jobs`, `search_people` and `search_posts` is no
> longer available. They remain callable but always return HTTP 410 and are never
> billed. `company()` still returns `featured_employees` (a small sample of
> staff), and `search_jobs()` with a company name substitutes for `company_jobs`.

### 12. TikTok Shop Product Research

```python
from scavio import ScavioClient

client = ScavioClient()

# Listings carry exact prices
results = client.tiktok_shop.search("phone case")
for p in results["data"]["products"][:5]:
    print(p["title"], p["price"]["current"], p["shop"]["shop_name"])

# Detail adds description, variants, stock and shipping -- but NOT a price
# (TikTok masks it), and it resolves only about 44% of the ids search returns.
# A 404 there is a normal outcome, not an error: skip the item, do not retry.
from scavio import NotFoundError

product_id = results["data"]["products"][0]["product_id"]
try:
    detail = client.tiktok_shop.product(product_id)
    print(detail["data"]["title"], len(detail["data"]["variants"]), "variants")
except NotFoundError:
    pass  # TikTok Shop has no detail data for this product; skip it, do not retry

reviews = client.tiktok_shop.product_reviews(product_id, page_size=200, sort="relevant")
catalog = client.tiktok_shop.shop_products("7495514739648989419")   # exact prices
tree = client.tiktok_shop.categories()
resolved = client.tiktok_shop.resolve("https://vt.tiktok.com/ZT2AHoGsE/")
```

### 13. Social Media Monitoring

```python
from scavio import ScavioClient

client = ScavioClient()

brand = "scavio"
reddit = client.reddit.search(brand)
tiktok = client.tiktok.search_videos(brand, count=5)

print(f"Reddit mentions ({len(reddit['data']['results'])}):")
for post in reddit["data"]["results"][:3]:
    print(f"  r/{post['subreddit']}: {post['title']}")

tiktok_videos = tiktok["data"].get("search_item_list", [])
print(f"\nTikTok mentions ({len(tiktok_videos)}):")
for v in tiktok_videos[:3]:
    desc = v["aweme_info"].get("desc", "No description")
    print(f"  {desc[:80]}")
```

### 14. Price Drop Alert

```python
from scavio import ScavioClient

client = ScavioClient()

product = client.walmart.product("123456789")
price = product["data"]["price"]
title = product["data"]["title"]

threshold = 50.00
if price and price < threshold:
    print(f"PRICE DROP: {title[:60]}")
    print(f"  Now ${price} (threshold: ${threshold})")
else:
    print(f"{title[:60]}: ${price}")
```

### 15. Async Multi-Source Search

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient() as client:
        google = await client.search("mechanical keyboard")
        amazon = await client.amazon.search("mechanical keyboard", country="us")

        print(f"Google: {len(google['organic_results'])} results")
        print(f"Amazon: {len(amazon['data']['products'])} products")

        for r in google["organic_results"][:3]:
            print(f"  Web: {r['title'][:60]}")
        for p in amazon["data"]["products"][:3]:
            print(f"  Amazon: ${p['price']} - {p['title'][:50]}")

asyncio.run(main())
```

### 16. Check API Usage

```python
from scavio import ScavioClient

client = ScavioClient()

usage = client.get_usage()
print(f"Plan: {usage['plan']}")
print(f"Credits remaining: {usage['credit_balance']}")
```

### 17. Read Any URL -- `extract()`

`extract` is a core capability, not a platform, so it is a top-level method:
`client.extract(url)`, never `client.extract.extract()`. It is the "read this
page" primitive an agent reaches for when the page is not on a site Scavio has
a dedicated namespace for.

```python
from scavio import ScavioClient

client = ScavioClient()

# Default: readability Markdown, normal mode. 1 credit.
page = client.extract("https://example.com/blog/post")["data"]
print(page["content_length"], "chars of", page["format"])
print(page["content"][:500])

# format="html" is the raw page; format="text" is the Markdown flattened.
raw = client.extract("https://example.com/blog/post", format="html")

# mode is the price-bearing parameter, and the only knob that matters on a
# hard target: "normal" (1 credit) -> "advanced", a full browser render
# (1 credit) -> "ultra", the hardest-target tier (2 credits).
hard = client.extract("https://example.com/spa", format="markdown", mode="ultra")

# Billing is charged only on a successful extraction: a dead link, a bot wall
# or a timeout costs nothing, so retrying up a tier is safe.
```

### 18. eBay Price Research -- Sold Listings, Not Asking Prices

Live listings tell you what sellers *want*. `sold=True` searches completed
listings that actually sold, which is what a pricing model needs.

```python
from scavio import ScavioClient

client = ScavioClient()

sold = client.ebay.search(
    query="airpods pro 2",
    sold=True,
    condition="used",
    per_page=240,          # 60, 120 or 240 only; anything else falls back to 60
    min_price=50,          # prices are numbers, so 49.99 is legal too
)["data"]

prices = sorted(p["price"] for p in sold["products"] if p.get("price"))
print("median sold price:", prices[len(prices) // 2])

# On the sold view eBay publishes no headline count, so total_results is null.
# Page with `page` until a page comes back empty rather than trusting a total.
assert sold["total_results"] is None

# On the LIVE view total_results is eBay's own estimate and an unstable one --
# four identical requests minutes apart reported 28k, 140k, 170k and 27k.
# Treat it as an order of magnitude, never as a count.

# `seller` works with no query at all, which is how you page a whole catalogue.
# ebay.seller() is a profile card only -- it cannot enumerate inventory.
catalogue = client.ebay.search(seller="mytechstore", page=1)["data"]
profile = client.ebay.seller("mytechstore")["data"]
```

### 19. Meta Ad Library -- Walking a Competitor's Whole Ad Set

Meta pages the ad library by cursor, and the first page is a different size
from the rest: 30 ads on page 1, then 10 per cursor page.

```python
from scavio import ScavioClient

client = ScavioClient()

ads, cursor = [], None
while True:
    # page_id is the advertiser's numeric Facebook Page id, as a string.
    page = client.meta_ads.advertiser("20531316728", cursor=cursor)["data"]
    ads.extend(page["ads"])
    if not page["has_next_page"]:
        break
    cursor = page["next_cursor"]

print(len(ads), "ads")

# Every page is 1 credit, and past the first 30 ads a page is 10 ads, so a deep
# walk costs roughly one credit per ten ads. Budget for depth.

# Keyword search pages the same way. total_results caps at 50000 with
# total_is_capped true, because Meta itself only reports ">50,000" -- never
# present it as an exact count.
first = client.meta_ads.search(
    "black friday", country="US", active_status="active"
)["data"]
if first["total_is_capped"]:
    print("more than", first["total_results"], "ads match")

# Spend, reach, impressions and the paid-for-by disclosure are political-only.
# On commercial ads they are null by design, not a bug.
political = client.meta_ads.search("vote", ad_type="political_and_issue_ads")["data"]

# The cursor is a self-contained blob: every other filter is ignored while it
# is set, so do not "change the filter and keep paging" -- start a new walk.
```

### 20. Costco -- Warehouse Prices, Stock, Gas, Coupons and Clearance

`costco` covers costco.com and costco.ca (`country="ca"`); `search`, `product`
and `warehouses` also take the international sites (uk, au, mx, jp, kr, tw).
Warehouse numbers come from `warehouses()`; pass one as `warehouse_id` to add
that warehouse's in-store price, stock status and price code to every search,
category or deals result.

```python
from scavio import ScavioClient

client = ScavioClient()

# Nearest warehouses to a US zip code, with hours, services and gas prices.
near = client.costco.warehouses(zip="10025", limit=3)["data"]

# Search with one warehouse's in-store price alongside the online price.
oil = client.costco.search("olive oil", warehouse_id="1062", page_size=5)["data"]
for item in oil["results"]:
    print(item["title"], item["price"], item["warehouse"]["price"])

# Online vs in-warehouse price at up to 10 warehouses, with discount, final
# price and promotion dates. 1 credit for up to 9 warehouses, 2 for 10.
prices = client.costco.prices(item_id="1492456", warehouse_ids=["1062", "1107"])["data"]
for row in prices["items"][0]["warehouses"]:
    print(row["warehouse_id"], row["price"], row["final_price"])

# In-warehouse stock status (a status, never a quantity). 1 credit per 5 warehouses.
stock = client.costco.availability("1492456", ["1062"])["data"]

# Regular, premium and diesel prices near a location, or at given warehouses.
gas = client.costco.gas(zip="90001")["data"]
for station in gas["stations"]:
    print(station["name"], station["prices"]["regular"], station["prices"]["premium"])

# The current member coupon book (US), and the deal feeds.
book = client.costco.coupons()["data"]
hunt = client.costco.deals("treasure_hunt")["data"]

# Markdown finder at one warehouse: .97 clearance and .00/.88 manager markdowns
# by default; add special_buy for .49/.79/.89 endings. The codes are the
# member-community decode -- Costco does not publish them.
marked_down = client.costco.clearance("1062", query="snacks")["data"]
print(marked_down["count"], "of", marked_down["products_scanned"], "items marked down")
```

### 21. Trustpilot -- Business Search, Profiles, Reviews and Categories

`trustpilot` finds businesses by keyword or category, reads a full profile
(TrustScore, rating distribution, reply rate and days to reply on negative
reviews, AI summary and topics when Trustpilot has them), and pages filtered
reviews. Every call costs 2 credits. `business()` and `reviews()` take exactly
one of `domain` or `url`.

```python
from scavio import ScavioClient

client = ScavioClient()

# Businesses matching a keyword, up to 100 per page. Email and phone appear
# only when the business published them.
found = client.trustpilot.search("vpn", country="US", page_size=10)["data"]
for biz in found["businesses"]:
    print(biz["name"], biz["domain"], biz["trust_score"], biz["review_count"], biz["email"])

# One profile with the rating distribution, reply behavior and 20 newest reviews.
profile = client.trustpilot.business(domain="nordvpn.com")["data"]
print(profile["trust_score"], profile["rating_distribution"])
print(profile["reply_behavior"]["reply_rate"], profile["reply_behavior"]["avg_days_to_reply"])
topic_ids = [t["id"] for t in profile["topics"]]  # feed these to reviews(topics=...)

# Filtered reviews, 20 per page. Trustpilot serves up to 10 pages (200 reviews)
# per filter combination; max_page says how far this one goes. Slice by stars,
# language, date_range, topics or search to reach more. total_filtered counts
# every match, so a date range doubles as review velocity.
bad = client.trustpilot.reviews(
    domain="nordvpn.com", stars=[1, 2], language="en", date_range="last30days"
)["data"]
print(bad["total_filtered"], "1-2 star reviews in 30 days; pages:", bad["max_page"])
for review in bad["reviews"]:
    print(review["rating"], review["title"], (review["reply"] or {}).get("text"))

# The category tree, then ranked businesses in one category. min_trust_score is
# a star-rating floor: Trustpilot rounds TrustScore to stars, so 4 includes 3.8+.
tree = client.trustpilot.categories()["data"]
print(tree["count"], "top-level,", tree["subcategory_count"], "subcategories")
ranked = client.trustpilot.category(
    "vpn_service", sort="reviews_count", min_trust_score=4, claimed_only=True
)["data"]
for biz in ranked["businesses"]:
    print(biz["name"], biz["trust_score"], biz["website"])

# One review by id, with the business it is about.
one = client.trustpilot.review("6aca2504b52cc4b518bf4b75")["data"]
print(one["review"]["text"], one["business"]["name"])
```

An unknown business, review or category returns a 404 (`NotFoundError`) and is
billed 2 credits. Trustpilot keeps no TrustScore history, so none is returned.

### 22. Realtor.com and Rightmove -- Listings, Sold Comps and Agents

`realtor` covers US listings (for sale, pending, for rent and sold) with up to
200 rows per call, full property detail, market stats and agents. `rightmove`
covers UK listings, England and Wales sold house prices since 1995 and agent
branches. Every call on both costs 1 credit.

Docs: Realtor.com [search](https://scavio.dev/docs/realtor-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [property](https://scavio.dev/docs/realtor-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [locations](https://scavio.dev/docs/realtor-locations?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [market](https://scavio.dev/docs/realtor-market?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agents](https://scavio.dev/docs/realtor-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agent](https://scavio.dev/docs/realtor-agent?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Realtor.com API](https://scavio.dev/realtor-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.
Rightmove [search](https://scavio.dev/docs/rightmove-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [property](https://scavio.dev/docs/rightmove-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [sold](https://scavio.dev/docs/rightmove-sold?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [sold property](https://scavio.dev/docs/rightmove-sold-property?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [locations](https://scavio.dev/docs/rightmove-locations?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agents](https://scavio.dev/docs/rightmove-agents?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [agent](https://scavio.dev/docs/rightmove-agent?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Rightmove API](https://scavio.dev/rightmove-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.

```python
from scavio import ScavioClient

client = ScavioClient()

# Sold land comps: 200 rows per call, filtered by lot size, price and recency.
# Realtor.com serves the first 10,000 results of a search; slice by price band,
# property type or area to go further. Sold prices are null in US non-disclosure
# states (Texas, Utah, Wyoming and others); sold dates still come back.
comps = client.realtor.search(
    location="Maricopa County, AZ",
    listing_status="sold",
    property_types=["land"],
    sold_within_days=365,
    lot_sqft_min=43560,
    page_size=200,
)["data"]
print(comps["total"], "sold; pages:", comps["max_page"])
for row in comps["listings"]:
    print(row["sold_price"], row["sold_date"], row["lot_sqft"], row["address"]["line"])

# Listing-text keyword watch, then one property in full. A listing must contain
# ALL the keywords you pass, so each extra keyword narrows the results.
shops = client.realtor.search(location="Austin, TX", keywords=["workshop"])["data"]
detail = client.realtor.property(property_id=shops["listings"][0]["property_id"])["data"]
print(detail["list_price"], detail["risk"]["flood_factor"], len(detail["property_history"]))

# Autocomplete -> market stats, and agents by ZIP code.
slug = client.realtor.locations("Austin")["data"]["locations"][0]["slug_id"]
market = client.realtor.market(slug)["data"]
print(market["median_listing_price"], market["median_days_on_market"])
agents = client.realtor.agents(postal_code="78744")["data"]
profile = client.realtor.agent(agents["agents"][0]["agent_id"])["data"]
print(profile["name"], profile["rating"], len(profile["reviews"]))

# Rightmove: resolve a place, search for sale (24-25 per page, up to 42 pages).
# There is no keyword filter; match on summary and key_features yourself.
loc = client.rightmove.locations("Bristol")["data"]["locations"][0]["location_id"]
homes = client.rightmove.search(location_id=loc, property_types=["terraced"], max_price=350000)
for home in homes["data"]["listings"]:
    print(home["price_display"], home["address"], home["tenure"])

# Sold prices since 1995 for an outcode (England and Wales only), then one
# address's full history.
sold = client.rightmove.sold("BS3", sold_within_years=5)["data"]
print(sold["summary"]["average_price_last_year"])
history = client.rightmove.sold_property(sold_id=sold["properties"][0]["sold_id"])["data"]
for sale in history["transactions"]:
    print(sale["date"], sale["price_display"], sale["tenure"], sale["percent_change"])

# Agent branches in an area, then one branch.
branches = client.rightmove.agents(location="Bristol")["data"]
branch = client.rightmove.agent(branch_id=branches["agents"][0]["branch_id"])["data"]
print(branch["name"], branch["listings"]["for_sale_count"], branch["listings"]["to_rent_count"])
```

An unknown property, listing, sold id, agent or branch returns a 404
(`NotFoundError`) and is billed 1 credit; a removed Rightmove listing is also a
404. Rightmove serves 42 search pages, 40 sold pages and 50 agent pages per
query.

### 23. Mercado Libre -- Listings, Products, Reviews, Questions and Best Sellers

`mercadolibre` covers Mercado Libre in Mexico, Argentina and Colombia and
Mercado Livre in Brazil (`country="mx"`, `"br"`, `"ar"` or `"co"`; prices come
back in MXN, BRL, ARS or COP). `reviews` costs 1 credit; `search`, `product`,
`questions` and `best_sellers` cost 2. Chile is not supported.

Docs: Mercado Libre [search](https://scavio.dev/docs/mercadolibre-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [product](https://scavio.dev/docs/mercadolibre-product?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [reviews](https://scavio.dev/docs/mercadolibre-reviews?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [questions](https://scavio.dev/docs/mercadolibre-questions?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [best sellers](https://scavio.dev/docs/mercadolibre-best-sellers?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme); overview at the [Mercado Libre API](https://scavio.dev/mercadolibre-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) page.

```python
from scavio import ScavioClient

client = ScavioClient()

# Search by keyword (about 48 rows per page, up to 42 pages, so about 2,000
# results per query; slice by price range, condition or seller to reach more).
found = client.mercadolibre.search(
    "iphone 15",
    country="mx",
    free_shipping=True,
    sort="price_asc",
)["data"]
print(found["total"], found["auto_applied_filters"])
for row in found["results"]:
    # sold_quantity_min is a lower bound ("+1000 vendidos"), never an exact count.
    print(row["price"], row["original_price"], row["sold_quantity_min"], row["title"])

# One catalog product: price, buy-box seller with reputation, star distribution.
product = client.mercadolibre.product(product_id="MLM1027172667")["data"]
print(product["price"], product["seller"]["nickname"], product["rating"]["distribution"])

# A seller's catalogue: the buy-box seller_id feeds a filtered search.
catalogue = client.mercadolibre.search(
    country="mx", seller_id=str(product["seller"]["seller_id"]), condition="new"
)["data"]

# Reviews (15 per page, 1 credit), e.g. only 1-star; original_text keeps the
# untranslated review and country says where it was written.
reviews = client.mercadolibre.reviews(product_id="MLM1027172667", rating=1)["data"]
for review in reviews["reviews"]:
    print(review["rating"], review["country"], review["text"])

# Buyer questions with the seller's answers; page with next_offset.
qa = client.mercadolibre.questions(product["item_id"])["data"]
for q in qa["questions"]:
    print(q["text"], "->", q["answer"]["text"] if q["answer"] else None)

# Top 20 best sellers in a category (mx, ar or co; not Brazil). The category
# prefix must match the country.
top = client.mercadolibre.best_sellers(product["category_id"], country="mx")["data"]
for row in top["results"]:
    print(row["rank"], row["price"], row["sold_label"], row["title"])
```

A zero-result search returns an empty page and is billed. An unknown product,
item or seller nickname returns a 404 (`NotFoundError`) and is billed, as does a
listing with no public questions. Only the buy-box seller is returned per
product, and Brazil and Argentina may auto-apply a "new" condition (listed in
`auto_applied_filters`).

## Error Handling

```python
from scavio import (
    ScavioClient,
    InvalidAPIKeyError,
    RateLimitError,
    InsufficientCreditsError,
    NotFoundError,
    BadRequestError,
    ScavioConnectionError,
    ScavioTimeoutError,
    ScavioAPIError,
    ScavioError,
)

client = ScavioClient(api_key="sk_...")

try:
    results = client.search("query")
except InvalidAPIKeyError:
    print("Check your API key")
except RateLimitError:
    print("Too many requests - upgrade your plan")
except InsufficientCreditsError:
    print("Out of credits - purchase more at dashboard.scavio.dev")
except ScavioAPIError as e:
    # Any other non-2xx response; inspect the details:
    print(e.status_code, e.response_body)
```

All exceptions inherit from `ScavioError`. HTTP errors (`BadRequestError` 400,
`InvalidAPIKeyError` 401, `InsufficientCreditsError` 402, `NotFoundError` 404,
`RateLimitError` 429, `ScavioAPIError` for anything else) carry `.status_code`
and `.response_body`. Network failures raise `ScavioConnectionError` /
`ScavioTimeoutError` after retries are exhausted.

## Configuration

```python
client = ScavioClient(
    api_key="sk_...",
    base_url="https://api.scavio.dev",  # custom base URL
    timeout=30.0,                        # request timeout in seconds
    max_requests_per_second=1,           # client-side rate limit (1-50)
    max_retries=2,                       # retries on 429/5xx/network (0 disables)
)
```

### Async client

The async client mirrors the sync one method-for-method. It keeps a single
pooled `httpx.AsyncClient` alive for its lifetime; close it with
`await client.aclose()` or use the async context manager.

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient(api_key="sk_...") as client:
        return await client.google.search("openai", gl="us")

asyncio.run(main())
```

## Integrations

Scavio works with popular AI/LLM frameworks:

- [LangChain](https://github.com/scavio-ai/langchain-scavio) -- `pip install langchain-scavio`
- [MCP Server](https://www.npmjs.com/package/@scavio/mcp-server) -- for Claude, Cursor, and other MCP clients
- [n8n](https://www.npmjs.com/package/n8n-nodes-scavio) -- no-code workflow automation

## API Reference

| Service | Endpoints | Credits |
|---------|-----------|---------|
| Google | `search`, `ai_mode`, `maps_search`, `maps_place`, `maps_reviews`, `shopping`, `shopping_product`, `shopping_stores`, `flights`, `hotels`, `hotels_detail`, `news`, `trends`, `trending` | 1 each |
| Amazon | `search`, `product`, `offers`, `options` | 1 each (`options` free) |
| Walmart | `search`, `product`, `stores`, `reviews`, `category`, `offers`, `seller`, `seller_products` | 1, except `search`/`category` on `domain="com.mx"` and store-targeted `search`/`product` (`delivery_zip` + `store_id`), which cost 2 |
| YouTube | `search`, `shorts`, `suggestions`, `video`, `metadata` (deprecated alias of `video`), `comments`, `comment_replies`, `transcript`, `related`, `channel_search`, `channel`, `channel_videos`, `channel_shorts`, `channel_community`, `channel_resolve`, `streams`, `community_post`, `community_post_comments` | `search`/`shorts` 2, `transcript` 5, `streams` 3, rest 1 each |
| Reddit | `search`, `search_suggestions`, `post`, `post_comments`, `comment_replies`, `subreddit`, `subreddit_posts`, `user`, `user_posts`, `user_comments`, `popular`, `trending`, `search_comments`, `search_subreddits` | 1 each |
| X | `search`, `tweet`, `tweet_comments`, `tweet_retweeters`, `user`, `user_tweets`, `user_replies`, `user_media`, `user_followers`, `user_followings`, `trending`, `search_communities`, `community`, `community_tweets` | 1 each |
| TikTok | `profile`, `user_posts`, `video`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings`, `trending_searches`, `trending_videos`, `search_suggestions`, `music`, `music_videos`, `search_music`, `music_chart`, `user_similar`, `user_playlists`, `playlist_videos`, `user_live`, `user_region` | 1 each |
| TikTok Shop | `search`, `search_suggestions`, `product`, `product_reviews`, `categories`, `category_products`, `shop_products`, `resolve` | 1 each |
| Instagram | `profile`, `user_posts`, `user_reels`, `user_tagged`, `user_stories`, `post`, `post_comments`, `comment_replies`, `search_users`, `search_hashtags`, `user_followers`, `user_followings` | `user_posts` 2, `post`/`comment_replies` 8, the other nine 10 each |
| LinkedIn | `person`, `person_about`, `person_posts`, `person_contact`, `company`, `company_posts`, `company_people`, `company_jobs`, `search_people`, `search_jobs`, `search_posts`, `job`, `post`, `post_comments` | `job` 30, `person_posts`/`company_posts`/`search_jobs`/`post_comments` 10 each, `person`/`person_about`/`company`/`post` 1 each; the five retired endpoints (`person_contact`, `company_people`, `company_jobs`, `search_people`, `search_posts`) return 410 and are never billed |
| Threads | `profile`, `user_posts`, `user_replies`, `post`, `post_comments`, `search_users` | 2, but `profile`/`user_posts`/`user_replies` cost 4 when addressed by `username` instead of `user_id` |
| Kuaishou | `profile`, `user_posts`, `user_live`, `user_resolve`, `video`, `video_comments`, `comment_replies`, `videos_batch`, `search`, `search_videos`, `search_users`, `search_live`, `tag_feed`, `trending` | priced per endpoint: `videos_batch` 40, `profile` and the four `search*` 10 each, `video` 2, the rest 1 |
| eBay | `search` (live or sold listings), `product`, `seller` | 1 each |
| Target | `search`, `category`, `product`, `reviews` | 1 each |
| Home Depot | `search`, `product`, `reviews` | 2 each |
| Zillow | `search`, `property`, `agent_reviews` | 1 each |
| Redfin | `search`, `property`, `market` | 1 each |
| Realtor.com | `search`, `property`, `locations`, `market`, `agents`, `agent` | 1 each |
| Rightmove | `locations` (start here), `search`, `property`, `sold`, `sold_property`, `agents`, `agent` | 1 each |
| Booking.com | `search`, `hotel`, `reviews` | 1 each |
| Tripadvisor | `locations` (start here), `search`, `location`, `reviews` | 2 each |
| Airbnb | `search`, `listing`, `reviews` | 1 each |
| Yelp | `search`, `business`, `reviews` | 2 each |
| Indeed | `search`, `job`, `company`, `company_reviews` | 2 each |
| Glassdoor | `companies` (start here), `company`, `reviews`, `salaries` | 1 each |
| Apple App Store | `search`, `app`, `reviews` | 1 each |
| Google Play | `search`, `app`, `reviews` | 2 each |
| SEC EDGAR | `lookup` (start here), `company`, `filings`, `concept`, `facts`, `search` | 1 each |
| Companies House | `search` (start here), `company`, `officers`, `filing_history` | 1 each |
| G2 | `search`, `product`, `reviews` | 5 each |
| Capterra | `search`, `product`, `reviews` | 2 each |
| Google Ads Transparency | `advertisers` (start here), `search`, `creative` | 1 each |
| Meta Ad Library | `search`, `advertiser`, `ad` | 1 each |
| Costco | `search`, `category`, `categories`, `product`, `prices`, `availability`, `reviews`, `warehouses`, `gas`, `coupons`, `deals`, `clearance`, `autocomplete` | 1 each, except `prices` (2 at 10 warehouses), `availability` (1 per 5 warehouses), `warehouses` (2 with `country="ca"`) and `gas` (2 by location on ca; by `warehouse_ids`, 1 per 5 on us and 2 per warehouse on ca) |
| Trustpilot | `search`, `business`, `reviews`, `categories`, `category`, `review` | 2 each |
| Mercado Libre | `search`, `product`, `reviews`, `questions`, `best_sellers` | `reviews` 1, the rest 2 each |
| Extract (core, not a namespace) | `client.extract(url)` | 1 for `mode="normal"` or `"advanced"`, 2 for `"ultra"`; only a successful extraction is billed |

Every method's full parameter list is available inline in your editor (typed
keyword arguments with docstrings). See the [API docs](https://scavio.dev/docs?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
for field-level details.

### Changed in 0.22.0

- **19 new methods across TikTok, YouTube, Reddit and X, 1 credit each.**
  - `tiktok`: `trending_searches()`, `trending_videos()` (about 6 videos per
    call whatever `count` says), `search_suggestions(keyword)`,
    `music(music_id)`, `music_videos(music_id)` (`count` is ignored upstream,
    about 14 per page), `search_music(keyword)`, `music_chart()` (Top 50 or
    Viral 50, one global chart), `user_similar(sec_user_id)`,
    `user_playlists(sec_user_id)`, `playlist_videos(playlist_id)`,
    `user_live(username)` (an unknown username is a billed 404) and
    `user_region(username)` (an unknown username is an unbilled 404; also
    returns `sec_user_id`). These return TikTok's raw payload: large numeric
    ids can lose precision as JSON numbers, so use `id_str` / `sec_uid`.
  - `youtube`: `community_post(post_id)`, `community_post_comments(post_id)`.
  - `reddit`: `search_comments(query)` (sort `RELEVANCE`, `HOT`, `TOP` or
    `NEW`), `search_subreddits(query)`.
  - `x`: `search_communities(keyword)`, `community(community_id)`,
    `community_tweets(community_id)` (ranking `Relevance` or `Recency`).
- `youtube.transcript` now costs 5 credits (was 8); the docstring says so.

```python
chart = client.tiktok.music_chart(chart="viral", count=10)
region = client.tiktok.user_region("mrbeast")
similar = client.tiktok.user_similar(region["data"]["sec_user_id"])
threads = client.reddit.search_comments("web scraping api", sort="NEW")
posts = client.x.community_tweets("1508567430188126209", ranking="Recency")
```

### Changed in 0.21.1

- README: Mercado Libre docs and landing page links; wording cleanup. No
  behavior changes.

### Changed in 0.21.0

- **New `mercadolibre` namespace, 5 methods.** `search` (keyword or seller in
  Mexico, Brazil, Argentina or Colombia; condition, price, discount, free
  shipping, Full fulfillment, official store and interest-free installment
  filters; relevance or price sort; 2 credits), `product` (buy-box seller,
  variations, star distribution, specs; 2), `reviews` (15 per page with a star
  filter; 1), `questions` (buyer questions with seller answers; 2) and
  `best_sellers` (top 20 in a category, not Brazil; 2). `country` is required
  on `search` and `best_sellers` and is keyword-only. See example 23 above.
- `realtor.search(keywords=...)` docstring: a listing must contain ALL the
  keywords, so each extra keyword narrows the results.

### Changed in 0.20.1

- README: Realtor.com and Rightmove docs links; Rightmove sold prices cover
  England and Wales only, and search pages return 24-25 rows (the
  `rightmove.search(page=...)` docstring now says so). No behavior changes.

### Changed in 0.20.0

- **New `realtor` namespace, 6 methods, 1 credit each.** `search` (for sale,
  pending, for rent or sold by location, radius or agent; price, beds, baths,
  sqft, lot, garage, HOA, year built, property type, recency, listing-text
  keywords and more; up to 200 rows per call), `property` (price and tax
  history, valuations, schools, risk, listing agent), `locations`, `market`,
  `agents` and `agent`.
- **New `rightmove` namespace, 7 methods, 1 credit each.** `locations`,
  `search` (buy or rent by location, place name or branch), `property`, `sold`
  (sale history since 1995 per address plus an area summary), `sold_property`,
  `agents` and `agent`. See example 22 above.

### Changed in 0.19.1

- `trustpilot.category(min_trust_score=...)` docstring corrected: the filter
  is a minimum star rating (3, 4 or 4.5). Trustpilot rounds TrustScore to
  stars, so 4 includes TrustScore 3.8 and up. No code changes.

### Changed in 0.19.0

- **New `trustpilot` namespace, 6 methods, 2 credits each.** `search`
  (businesses by keyword, up to 100 per page), `business` (full profile by
  domain or Trustpilot URL), `reviews` (stars, language, date range, sort,
  verified-only, with-replies, topics and text filters; up to 200 per filter
  combination), `categories` (the tree or a name lookup), `category` (ranked
  businesses with sort, minimum star rating and claimed-only) and `review` (one
  review by id). See example 21 above.

### Changed in 0.18.1

- Documentation links only; no code changes. The client already identifies
  itself on every call with `User-Agent: scavio-python/<version>` and
  `X-Client-Source: scavio-python`.

### Changed in 0.18.0

- **New `costco` namespace, 13 methods.** `search`, `category`, `categories`,
  `product` (up to 20 ids per call), `prices` (online vs in-warehouse price at up
  to 10 warehouses), `availability` (in-warehouse stock status), `reviews`,
  `warehouses`, `gas`, `coupons` (the member coupon book), `deals`
  (new, while_supplies_last, treasure_hunt, member_favorites, online_only,
  on_sale), `clearance` (price-code markdown finder) and `autocomplete`. See
  example 20 above.

### Changed in 0.17.0

- **Walmart store targeting.** `walmart.stores(zipcode, domain=...)` is new: it
  returns the Walmart stores near a US ZIP (walmart.com) or a Canadian postal
  code (`domain="ca"`, walmart.ca), nearest first, each with its `store_id`.
  Pass that `store_id` together with `delivery_zip` to `walmart.search()` or
  `walmart.product()` on the same domain to get that store's assortment and
  availability; `data.location` echoes the store used. Store-targeted calls
  cost 2 credits and take 10-60 seconds, so give them a generous timeout.
  `walmart.product()` also accepts `domain="ca"`, together with a store pair.

  ```python
  stores = client.walmart.stores("50036")
  store_id = stores["data"]["stores"][0]["store_id"]  # "1389", Boone Supercenter
  milk = client.walmart.search("whole milk", delivery_zip="50036", store_id=store_id)
  print(milk["data"]["location"])  # {"city": "Boone", "state": "IA", "store_id": "1389", ...}
  ```
- `delivery_zip` and `store_id` are no longer retired; `device` is now the only
  retired Walmart parameter.

### Changed in 0.16.0

- **`max_requests_per_second` now accepts up to 50** (it was capped at 10),
  matching the raised per-plan request limits -- the top plan allows 50, so
  the old ceiling rejected a value the plan entitled you to. The default is
  still 1, and the bound now lives in one place
  (`scavio._ratelimit.MAX_REQUESTS_PER_SECOND`) shared by the sync and async
  clients.

### Changed in 0.15.0

- **21 new namespaces with 85 endpoints**: Threads, Kuaishou, eBay, Target,
  Home Depot, Zillow, Redfin, Booking.com, Tripadvisor, Airbnb, Yelp, Indeed,
  Glassdoor, Apple App Store, Google Play, SEC EDGAR, Companies House, G2,
  Capterra, Google Ads Transparency and the Meta Ad Library. With the Walmart
  rebuild and `extract` below, that is 93 endpoints in this batch and 195 in the
  SDK. Every method is typed and documented inline, on both the sync and async
  clients.
- **`client.extract(url, format=..., mode=...)` is new, and is a top-level
  method, not a namespace.** Reading an arbitrary URL is a core capability
  rather than a platform, so it is `client.extract(...)`, never
  `client.extract.extract(...)`.
- **Walmart grew from 2 endpoints to 7** (`reviews`, `category`, `offers`,
  `seller`, `seller_products` are new) and `search`/`product` changed shape.
  `device`, `delivery_zip` and `store_id` are retired: the API answers 200 with
  a top-level `warnings` array if you send them through `**extra`. `domain`
  (`com` | `ca` | `com.mx`) is new on `search` and `category`, and it is the
  price-bearing parameter. `page` supersedes `start_page`, which stays as a
  deprecated alias.
- **Walmart `min_price` / `max_price` widened from `int` to `float`.** The
  backend was always `z.number()`, so `19.99` was always accepted; the old
  annotation was simply wrong. No runtime behaviour changed.
- **Four surfaces are body-priced and their docstrings say so** instead of
  quoting a flat price: Walmart (`com.mx` costs 2), Threads (4 credits when
  addressed by `username` instead of `user_id`), Kuaishou (1, 2, 10 or 40 per
  endpoint) and `extract` (`mode="ultra"` costs 2).
- Some caveats worth knowing before you write a loop: eBay `sold=True` returns
  `total_results: null`; Meta Ad Library pages are 30 ads then 10, and the
  cursor ignores every other filter; Capterra `search` does not paginate at all;
  Apple App Store `search` has no pagination either (raise `limit`, up to 200);
  Airbnb prices exist only on `search`, never on `listing`.

### Changed in 0.14.0

- `reddit.post()` now takes `post_id` as well as `url` -- pass either one. `url`
  stays the first positional argument, so existing calls are unaffected.
  The response is a flat post object and carries no comments; use
  `reddit.post_comments()` for those.
- `youtube.shorts(sort_by=...)` is now typed as
  `relevance | date | view_count | rating` instead of a free-form string.
- `youtube.search()` lost its `location` flag. It was never part of the backend
  schema, so it was silently dropped rather than filtering anything.

### Amazon changed in 0.12.0 (breaking)

The Amazon API now returns a normalized shape instead of the previous raw
payload.

- `search` returns `{query, page, total_results, total_results_text, count, products[], filters[], related_searches[]}`.
  Each product is `{asin, title, url, image, price, currency, rating, reviews_count, is_sponsored, position, badge, sales_volume, delivery{is_free, date, fastest_date}}`.
- `product` returns flat fields: `price`, `list_price`, `currency`, `rating`, `reviews_count`, `features`, `images`, `videos`, `variants`, `specifications`, `best_sellers_rank`, `shipping`, and more. The old `buybox[]` array no longer exists -- use `offers` for per-seller pricing.
- `offers` is new: every seller for one ASIN, with `price`, `condition`, `seller_name`, `is_buy_box_winner`, `is_fulfilled_by_amazon`, and delivery windows.
- `country` (ISO 3166-1 alpha-2: `us`, `gb`, `de`) is the marketplace selector and replaces `domain`. `page` replaces `start_page`. The old names still work as deprecated aliases.
- Nine parameters were removed: `language`, `currency`, `device`, `sort_by`, `pages`, `category_id`, `merchant_id`, `zip_code`, `autoselect_variant`. `sort_by` in particular was verified to be ignored by the marketplace, so result sorting is not available at any layer. Sending one of them anyway (via `**extra`) still returns 200, with a top-level `warnings` array explaining what was ignored.
- `options` still returns `domains` and `countries`; `languages` and `currencies` are now always empty, because neither is a request parameter any more.

## Links

- [Website](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
- [Documentation](https://docs.scavio.dev)
- [Dashboard & API Keys](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
- [API Reference](https://docs.scavio.dev/api-reference)
- [Compare Scavio vs alternatives](https://scavio.dev/compare?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)

## License

MIT


## About Scavio

[Scavio](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) is a unified [search API](https://scavio.dev/docs/search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) built for AI agents — one API key, structured JSON. A real-time [Tavily alternative](https://scavio.dev/alternatives/tavily?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [SerpAPI alternative](https://scavio.dev/alternatives/serpapi?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) with data from:

- [Google Search API](https://scavio.dev/google-search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — SERP results, news, images, maps, and knowledge graph
- [Amazon Product API](https://scavio.dev/amazon-product-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [Walmart Product API](https://scavio.dev/walmart-product-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — product search and details
- [YouTube API](https://scavio.dev/youtube-transcript-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), [TikTok API](https://scavio.dev/tiktok-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme), and [Instagram API](https://scavio.dev/instagram-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — video and social media data
- [TikTok Shop API](https://scavio.dev/docs/tiktok-shop-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — product search, detail, reviews, categories, and shop catalogs
- [Reddit API](https://scavio.dev/reddit-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — posts, comments, subreddits, and trending
- [X API](https://scavio.dev/docs/x-search?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and [LinkedIn API](https://scavio.dev/docs/linkedin-person?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) — tweets, profiles, companies, and jobs

For a detailed head-to-head breakdown, see [Tavily vs Scavio](https://scavio.dev/compare/tavily/vs-scavio?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

Get a free [API key](https://dashboard.scavio.dev/sign-up?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) and explore the [documentation](https://scavio.dev/docs/introduction?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).
