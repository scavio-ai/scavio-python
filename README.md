# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) Search API. Access real-time data from 73 sources -- Google, ChatGPT, Gemini, Amazon, Walmart, Costco, Best Buy, TCGplayer, Vinted, Macy's, Saks Fifth Avenue, Kohl's, JCPenney, Dick's Sporting Goods, Foot Locker, Fanatics, Nordstrom, Nordstrom Rack, Lowe's, Sam's Club, Canadian Tire, Dollar General, Sephora, Ulta Beauty, ALDI, Micro Center, Walgreens, CVS, Whole Foods Market, Harbor Freight, PetSmart, Petco, iHerb, Chewy, Menards, HEB, Kroger, Carrefour, Allegro, Spec's, Decathlon, Mercado Libre, eBay, Target, Home Depot, YouTube, Reddit, X, TikTok, TikTok Shop, Instagram, LinkedIn, Threads, Kuaishou, Zillow, Redfin, Realtor.com, Rightmove, Booking.com, Tripadvisor, Airbnb, Yelp, Indeed, Glassdoor, the Apple App Store, Google Play, SEC EDGAR, Companies House, G2, Capterra, Trustpilot, Google Ads Transparency and the Meta Ad Library -- plus `extract` for reading any URL and for mapping, crawling or batch-extracting whole websites, all with a single API key. Built for AI agents, LLM applications, and data pipelines.

> One API key, 60 data sources, 355 endpoints, structured JSON with knowledge graphs. A powerful alternative to Tavily, SerpAPI, and ScraperAPI for developers who need more than just web search.

## Why Scavio

| Feature | Scavio | Tavily | SerpAPI | ScraperAPI |
|---------|--------|--------|---------|------------|
| Google Search | Yes | Yes | Yes | Yes |
| ChatGPT and Gemini Answers with Cited Sources | Yes | No | No | No |
| Amazon Products | Yes | No | Yes | No |
| Walmart Products | Yes | No | No | No |
| Costco Warehouse Prices, Stock, Gas and Coupons (13 endpoints) | Yes | No | No | No |
| Store-Level Prices and Stock (Lowe's, Sam's Club, Canadian Tire, Dollar General; 21 endpoints) | Yes | No | No | No |
| Beauty, Pharmacy, Grocery and Electronics Stores (Sephora, Ulta Beauty, ALDI, Micro Center, Walgreens, CVS; 20 endpoints) | Yes | No | No | No |
| Grocery, Pet, Supplement and Hardware Stores (Whole Foods Market, Harbor Freight, PetSmart, Petco, iHerb, Chewy, Menards; 33 endpoints) | Yes | No | No | No |
| Nordstrom Products, Reviews, Categories, Brands, Store Pickup and Store Locator (8 endpoints) | Yes | No | No | No |
| Nordstrom Rack Clearance, Flash Events, Products, Reviews, Store Pickup and Store Locator (8 endpoints) | Yes | No | No | No |
| Best Buy Products, Open-Box Prices, Store Pickup, Deal of the Day, Reviews and Batch Prices (9 endpoints) | Yes | No | No | No |
| TCGplayer Card Market Prices, Price History, Recent Sales, Listings, Set Price Guides and Sellers (13 endpoints) | Yes | No | No | No |
| Vinted Listings, Prices, Sellers, Brands and Categories across 27 country sites (9 endpoints) | Yes | No | No | No |
| Macy's Products, Prices, Deals, Reviews, Brand Pages and Store Pickup (9 endpoints) | Yes | No | No | No |
| Saks Fifth Avenue Designer Sale Prices, Products, Stock, Designer Pages and Store Pickup (9 endpoints) | Yes | No | No | No |
| Kohl's Clearance, Sale Prices, Kohl's Cash, Coupon Codes and Store Pickup Units (9 endpoints) | Yes | No | No | No |
| JCPenney Clearance, Sale Prices, Coupon Codes, Store Unit Counts, Reviews and Q&A (11 endpoints) | Yes | No | No | No |
| Dick's Sporting Goods Clearance, Per-Size Prices, Store Unit Counts and Reviews (9 endpoints) | Yes | No | No | No |
| Foot Locker Release Calendar, Size Availability, Sale Prices, Reviews and Q&A (13 markets; 10 endpoints) | Yes | No | No | No |
| Fanatics Merchandise: Jersey Sale, Clearance and With-Code Prices, Size Stock Levels, League Stores and Reviews (8 markets; 5 endpoints) | Yes | No | No | No |
| Carrefour Grocery Prices by Store, Promotions, Nutri-Score, Stores and Fuel Prices (France, Argentina, Romania, Belgium; 9 endpoints) | Yes | No | No | No |
| Allegro Offers, Every Seller's Price, Sellers, Sold Counts and Auctions (Poland, Czechia, Slovakia, Hungary; 7 endpoints) | Yes | No | No | No |
| Trustpilot Businesses and Reviews (6 endpoints) | Yes | No | No | No |
| Mercado Libre Listings, Reviews and Best Sellers (MX, BR, AR, CO; 5 endpoints) | Yes | No | No | No |
| YouTube Search | Yes | No | Yes | No |
| Reddit Data (12 endpoints) | Yes | No | No | No |
| X Data (11 endpoints) | Yes | No | No | No |
| TikTok Data (24 endpoints) | Yes | No | No | No |
| TikTok Shop Data (8 endpoints) | Yes | No | No | No |
| Instagram Data (20 endpoints) | Yes | No | No | No |
| LinkedIn Data (9 endpoints) | Yes | No | No | No |
| eBay Sold-Listing Price History | Yes | No | No | No |
| Real Estate (Zillow + Redfin + Realtor.com + Rightmove, 19 endpoints) | Yes | No | No | No |
| UK Sold House Prices since 1995 (Rightmove, England and Wales) | Yes | No | No | No |
| Travel (Booking + Airbnb + Tripadvisor, 10 endpoints) | Yes | No | No | No |
| Jobs & Employers (Indeed + Glassdoor, 8 endpoints) | Yes | No | No | No |
| Ad Transparency (Meta + Google, 6 endpoints) | Yes | No | No | No |
| Filings (SEC EDGAR + Companies House, 10 endpoints) | Yes | No | No | No |
| Read Any URL (`extract`) | Yes | Yes | No | Yes |
| Data Sources | 60 | 1 | 1 per plan | 1 |
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

# Local rank tracking: web_only=True returns Google's Web results (organic
# only, ranked for location). The standard page localizes only the local pack;
# call again without web_only when you also need local_results.
local = client.google.search("emergency plumber", location="Austin,Texas,United States", web_only=True)

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

### 4b. Migrating from the Google Custom Search JSON API -- `google.custom_search`

`google.custom_search` takes the Custom Search JSON API (`cse.list`) parameters and returns
the same `customsearch#search` response: `items[]` with `title`, `link`, `snippet` and
`displayLink`, `searchInformation.totalResults`, and `queries.nextPage`. Parsing code written
for the Custom Search JSON API keeps working. 1 credit per call.

```python
results = client.google.custom_search(
    "abortcontroller fetch timeout",
    num=5,
    site_search="stackoverflow.com",   # enforced on the returned results
    date_restrict="y1",
)
for item in results.get("items", []):
    print(item["displayLink"], item["title"], item["link"])
next_page = results["queries"].get("nextPage", [{}])[0].get("startIndex")
```

Not using this SDK? Keep your existing Custom Search code and change the host:
`https://api.scavio.dev/customsearch/v1?key=YOUR_SCAVIO_KEY&q=...`. `cx` is accepted and
ignored (use `site_search` to restrict). Parameters that cannot be honoured (image search,
`sort`, `rights`) raise `BadRequestError` instead of being silently dropped. For the full SERP
(knowledge graph, AI overview, People Also Ask) use `google.search`.
[Docs](https://scavio.dev/docs/google-custom-search-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

### 4c. AI Visibility -- What ChatGPT and Gemini Recommend -- `chatgpt.prompt` / `gemini.prompt`

Send the prompt a buyer would ask and get the answer the assistant gives: the full Markdown
answer, the pages it cites, the web searches it ran (ChatGPT) and the products it recommended.
Both return the same shape under `data`, so one parser tracks both. ChatGPT costs 2 credits and
Gemini 5 credits per answered prompt; a failed prompt is not charged. Answers take 10-40 seconds, so both methods raise the
request timeout to 120s when your client's is shorter.

```python
prompt = "What are the best CRM tools for small agencies?"

for res in (client.chatgpt.prompt(prompt, country="us"), client.gemini.prompt(prompt)):
    data = res["data"]
    answer = data["answer"]["markdown"]
    print(data["platform"], "mentions HubSpot:", "HubSpot" in answer)
    print("  cited:", [s["url"] for s in data["sources"]][:5])
    print("  products:", [p["title"] for p in data["shopping"]])

# ChatGPT also reports the web searches it ran and each source's title and publisher
data = client.chatgpt.prompt(prompt)["data"]
print(data["search_queries"])
print([(s["source"], s["title"]) for s in data["sources"]][:5])
```

[ChatGPT docs](https://scavio.dev/docs/chatgpt-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme) |
[Gemini docs](https://scavio.dev/docs/gemini-api?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme).

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

# Profile and reels: typically 1 credit each; most other calls 2
profile = client.instagram.profile(username="nike")
user = profile["data"]
print(f"@{user['username']} - {user['follower_count']:,} followers")

posts = client.instagram.user_posts(username="nike", count=12)
reels = client.instagram.user_reels(username="nike")
hashtags = client.instagram.search_hashtags("fashion")

# Highlights, similar accounts, likers, and Reels / audio / place search
highlights = client.instagram.user_highlights(username="natgeo")
reels_found = client.instagram.search_reels("latte art")
tracks = client.instagram.search_music("espresso")
places = client.instagram.search_locations("blue bottle coffee")
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

`extract` is a core capability, not a platform. `client.extract(url)` reads one
page; the same `client.extract` object also maps, crawls and batch-extracts
whole sites (example 17b). It is the "read this page" primitive an agent
reaches for when the page is not on a site Scavio has a dedicated namespace for.

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
# hard target: "normal" (1 credit) -> "advanced" for JavaScript-built pages
# (1 credit) -> "ultra" for the hardest pages (2 credits).
hard = client.extract("https://example.com/spa", format="markdown", mode="ultra")

# Billing is charged only on a successful extraction: a dead link, a bot wall
# or a timeout costs nothing, so retrying up a tier is safe.
```

### 17b. Map, Crawl and Batch-Extract Whole Sites -- `extract.map / crawl / batch`

Three multi-page operations hang off `client.extract`:

| Call | What it returns | Price |
|---|---|---|
| `extract.map(url, ...)` | A site's page URLs from its sitemaps and start page, deduplicated and path-filtered (synchronous) | 1 credit on the normal tier (up to 2 on `advanced`, up to 10 on `ultra`) |
| `extract.crawl(url, ...)` | A job that discovers and extracts same-site pages breadth-first, each as Markdown, text or HTML | Per **successful** page at extract's price: 1 (`normal`, `advanced`) or 2 (`ultra`) |
| `extract.batch(urls, ...)` | A job that extracts a list of URLs, results in input order | Same per-page price; invalid URLs are reported and never billed |
| `extract.crawl_status(job_id)` / `extract.batch_status(job_id)` | Progress (`status`, `pages`, `credits_used`, `stopped_reason`) and one page of results with `next_cursor` | Free |
| `extract.cancel_crawl(job_id)` / `extract.cancel_batch(job_id)` | Stops a queued or running job; results so far stay available (409 if it already finished) | Free |

Failed and skipped pages cost nothing, starting a job costs nothing, and credits
are taken page by page: if your balance runs out the job stops cleanly with
`stopped_reason="insufficient_credits"`. robots.txt is always obeyed for map
and crawl. A crawl stays on the start URL's site (subdomains optional via
`allow_subdomains=True`) and visits URLs under the start path first. Results
are kept for 3 days after a job finishes (up to 2 MB per page, 250 MB per job);
a job runs for at most 6 hours.

| Plan | Max pages per crawl | Active jobs | URLs per batch |
|---|---|---|---|
| Free | 10 | 1 | 10 |
| PAYG | 100 | 1 | 50 |
| Project | 500 | 2 | 100 |
| Bootstrap | 2,000 | 3 | 500 |
| Startup | 5,000 | 5 | 1,000 |
| Growth | 10,000 | 10 | 1,000 |

Starting a job beyond your active-job limit raises `RateLimitError` (429).

```python
from scavio import ScavioClient

client = ScavioClient()

# Map: every URL on a site, filtered. Synchronous, 1 credit.
site = client.extract.map("https://scavio.dev", include_paths=["/docs/**"], limit=200)
for link in site["data"]["links"]:
    print(link["url"], link["source"], link.get("lastmod"))

# Crawl and wait: polls until the job finishes, then pages through every
# result for you. Two pages here, so 2 credits on the normal tier.
crawl = client.extract.crawl("https://scavio.dev/docs", max_pages=2, wait=True)
for page in crawl["data"]["results"]:
    print(page["url"], page["status"], page["content_length"])

# Or start it and poll yourself (better for large crawls).
job = client.extract.crawl(
    "https://example.com/blog",
    max_pages=500,
    max_depth=2,
    exclude_paths=["/blog/tag/**"],
    format="markdown",
)["data"]
status = client.extract.crawl_status(job["id"], include_content=False)
print(status["data"]["status"], status["data"]["pages"])

# Page through results with next_cursor (1-100 per call, default 25).
cursor = None
while True:
    page = client.extract.crawl_status(job["id"], cursor=cursor, limit=100)["data"]
    for result in page["results"]:
        ...  # result["url"], result["status"], result["content"]
    cursor = page["next_cursor"]
    if not cursor:
        break

# Batch: a list of URLs in one job, results in input order.
batch = client.extract.batch(
    ["https://example.com/a", "https://example.com/b"], format="text", wait=True
)
print(batch["data"]["pages"])
```

`wait=True` is a convenience: it polls every `poll_interval` seconds (default
2) and returns `{"data": {...final status..., "results": [...every page...],
"next_cursor": None}, "created": {...the job as created...}}`. Pass
`wait_timeout=` (seconds) to bound it; on expiry it raises
`ScavioJobTimeoutError`, whose `job_id` you can keep polling, while the job
keeps running on the server. Without `wait` you get the queued job back at once
(`id`, `status`, `status_url`, `credits_per_page`, and for batch `urls_count`
and `invalid_urls`).

Every crawl and batch POST carries an `Idempotency-Key` header. Pass your own
with `idempotency_key=` to make a retried request return the original job
within 24 hours; when you pass none, the SDK generates one per call so its own
automatic retries never start a second job. The async client has the same
surface: `await client.extract.crawl(...)`.

#### Completion webhooks

Pass `webhook_url="https://..."` to `crawl` or `batch` and Scavio POSTs the
final job status there when it completes, fails or is cancelled (retried after
30 seconds and 5 minutes on failure). The job creation response carries a
`webhook_secret`, returned only once; store it. Each delivery is signed with
`Scavio-Signature: t=<unix>,v1=<hex>`, an HMAC-SHA256 of `"<t>.<raw body>"`.
Verify it with `scavio.verify_webhook`, passing the RAW request body:

```python
import scavio

job = client.extract.crawl(
    "https://example.com/docs", webhook_url="https://hooks.example.com/scavio"
)["data"]
secret = job["webhook_secret"]  # store it: it is returned only once

# In your webhook handler (Flask shown):
from flask import Flask, abort, request

app = Flask(__name__)

@app.post("/scavio")
def scavio_webhook():
    if not scavio.verify_webhook(
        secret, request.headers.get("Scavio-Signature"), request.get_data()
    ):
        abort(401)
    event = request.get_json()
    print(event["id"], event["status"])
    return "", 204
```

`verify_webhook(secret, header, body, tolerance=300)` returns `False` for a
missing, malformed, tampered or stale (older than `tolerance` seconds)
signature, and compares in constant time.

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
    # review_count is null when the page shows none (most sponsored rows).
    print(row["price"], row["brand"], row["rating"], row["review_count"], row["sold_quantity_min"], row["title"])

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

### 24. Store-Level Retail -- Lowe's, Sam's Club, Canadian Tire and Dollar General

Four retailers whose prices and stock are per store. Each answers for ONE
store you choose: find its number with the locator (`lowes.stores`,
`sams_club.clubs`, `canadian_tire.stores`, `dollar_general.stores`) and pass it
on every call. Lowe's `search`, `product` and `stores` cost 2 credits and
`reviews` 1; every Sam's Club, Canadian Tire and Dollar General method costs 1.

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Lowe's: store_id AND that store's own ZIP are required on search/product.
store = client.lowes.stores("28117", limit=1)["data"]["stores"][0]
sid, zip_code = store["store_id"], store["address"]["postal_code"]

drills = client.lowes.search(sid, zip_code, query="cordless drill")["data"]
for p in drills["products"]:
    print(p["item_id"], p["price"], p["original_price"], p["stock_quantity"], p["title"])

# Deals are search(on_sale=True); there is no clearance endpoint.
deals = client.lowes.search(sid, zip_code, query="cordless drill", on_sale=True)["data"]

item = client.lowes.product("5016412045", sid, zip_code)["data"]
print(item["price"], item["stock_quantity"], item["aisle_locations"])
for near in item["pickup"]["nearby_stores"]:
    print(near["store_id"], near["distance_miles"], near["quantity"])

reviews = client.lowes.reviews("5016412045", sort="most_helpful")["data"]  # 1 credit
for r in reviews["reviews"]:
    print(r["rating"], r["verified_purchase"], r["title"])

# --- Sam's Club: search, savings and category answer for a club picked by
# location (echoed in data.club). For one specific club, use product(club_id=).
club = client.sams_club.clubs("75201", limit=1)["data"]["clubs"][0]
found = client.sams_club.search("paper towels", sort="price_low")["data"]
for p in found["products"]:
    print(p["item_id"], p["price"], p["was_price"], p["availability_status"], p["title"])

product = client.sams_club.product("15325822107", club_id=club["club_id"])["data"]
print(product["club_price"]["price"], product["in_stock_at_club"], product["aisle"])
for option in product["fulfillment"]["options"]:
    # available_quantity is capped at 8 by the site: 8 means 8 or more.
    print(option["method"], option["availability_status"], option["available_quantity"])

savings = client.sams_club.savings(sort="top_selling")["data"]        # Instant Savings
clearance = client.sams_club.category("1150109")["data"]              # clearance
reviews = client.sams_club.reviews("15325822107", sort="lowest")["data"]

# --- Canadian Tire: prices are in CAD and differ by store and province.
stores = client.canadian_tire.stores(postal_code="M5V 2T6", sku="0438858")["data"]
for s in stores["stores"]:
    print(s["store_id"], s["name"], s["distance_km"], s["quantity"], s["aisle"])

found = client.canadian_tire.search("600", query="dewalt drill")["data"]
for p in found["products"]:
    print(p["code"], p["sku"], p["price"], p["was_price"], p["store_quantity"], p["title"])

detail = client.canadian_tire.product("0547273P", "600")["data"]
stock = client.canadian_tire.availability("600", ["0438858", "0547273"])["data"]  # up to 50 SKUs
for i in stock["items"]:
    print(i["sku"], i["price"], i["is_clearance"], i["quantity"], i["aisle"])
print("unknown:", stock["not_found"])

clearance = client.canadian_tire.clearance("600")["data"]             # in-stock only by default
sale = client.canadian_tire.deals("600", "sale")["data"]              # or instant_rebate, special_buy, loyalty

# --- Dollar General: one call gives a product's unit count at up to 25 stores.
nearby = client.dollar_general.stores(zip="75203", upc="030772156629")["data"]
for s in nearby["stores"]:
    print(s["store_id"], s["address"], s["city"], s["distance_miles"], s["quantity"], s["in_stock"])

found = client.dollar_general.search("paper towels", "12629", in_stock_only=True)["data"]
for p in found["products"]:
    print(p["upc"], p["price"], p["original_price"], p["available_quantity"], p["title"])

item = client.dollar_general.product("030772156629", "12629")["data"]
print(item["price"], item["available_quantity"], item["nearby_stores_with_stock"])

# Clearance items carry the current price only (no was-price).
on_sale = client.dollar_general.deals("12629", "on_sale")["data"]
clearance = client.dollar_general.deals("12629", "clearance")["data"]
for c in client.dollar_general.coupons()["data"]["coupons"]:
    print(c["summary"], c["brand"], c["expiration_date"])
```

Canadian Tire and Dollar General return a rating and review count but no review
text. Sam's Club's search, savings and category results reflect the club in
`data.club`, not a club you pick.

### 25. US Retail -- Sephora, Ulta Beauty, ALDI, Micro Center, Walgreens and CVS

Six US retailers. Sephora and Ulta Beauty carry per-shade prices and stock;
ALDI prices are per store and per shopping mode; Micro Center stock is per
store; Walgreens and CVS prices are national while stock is per store. Every
method costs 1 credit except Micro Center `search` and `product` (2), Walgreens
`search`, `product` and `stores` (2) and Walgreens `stock` (4).

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Sephora: search, then one product with every shade and the review summary.
found = client.sephora.search("lipstick", sort="best_selling", zip="10001")["data"]
for p in found["products"]:
    print(p["product_id"], p["brand"], p["price"], p["rating"], p["same_day_eligible"], p["name"])

lips = client.sephora.category("lipstick")["data"]                  # same product shape
item = client.sephora.product(url=found["products"][0]["url"])["data"]  # url is faster than product_id
print(item["review_summary"])                                       # no review text
for s in item["review_sentiments"]:
    print(s["type"], s["sentiment"], s["count"])                    # pros / cons with counts
for sku in item["skus"]:
    print(sku["sku_id"], sku["variation_value"], sku["price"], sku["in_stock"], sku["only_few_left"])

# --- Ulta Beauty: stores() is in stock / out of stock at the 10 stores nearest a ZIP.
found = client.ulta.search("lipstick")["data"]
p = found["products"][0]
print(p["product_id"], p["sku_id"], p["list_price"], p["sale_price"], p["variant_label"])

detail = client.ulta.product(p["url"])["data"]
print(detail["availability"], detail["gtin"], [v["sku_id"] for v in detail["variants"]])
stores = client.ulta.stores(p["product_id"], p["sku_id"], "10001")["data"]
for s in stores["stores"]:
    print(s["store_id"], s["name"], s["distance_miles"], s["in_stock"], s["availability"])

# --- ALDI: prices are one store's and one shopping mode's. service_type is
# instore (default, the shelf price), pickup or delivery (often higher).
store = client.aldi.stores("33131", limit=1)["data"]["stores"][0]
milk = client.aldi.search("milk", store_id=store["store_id"])["data"]
for p in milk["products"]:
    print(p["product_id"], p["price"], p["was_price"], p["unit_price"], p["in_store_location"], p["name"])

online = client.aldi.search("milk", zip="33131", service_type="delivery")["data"]  # nearest store
item = client.aldi.product("16902710", store_id=store["store_id"])["data"]
print(item["price"], item["in_stock"], item["ingredients"], item["warnings"])

# --- Micro Center: stock is per 3-digit store_id; omit it for the web store
# (029, shippable items only). Counts are capped at 25+ (quantity_capped).
dallas = [s for s in client.micro_center.stores(state="TX")["data"]["stores"] if s["name"] == "Dallas"][0]
gpus = client.micro_center.search(query="rtx 5070", store_id=dallas["store_id"])["data"]   # 2 credits
for p in gpus["products"]:
    print(p["product_id"], p["price"], p["stock"]["label"], p["stock"]["quantity"], p["open_box"])

gpu = client.micro_center.product("691231", store_id=dallas["store_id"])["data"]          # 2 credits
print(gpu["selected_store"]["stock"], gpu["selected_store"]["open_box"])
print([s["store_id"] for s in gpu["stores_in_stock"] if s["in_stock"]])                  # yes/no per store

# --- Walgreens: prices are national; stock() checks up to 20 stores in one call.
nearby = client.walgreens.stores(zip="60614", limit=5)["data"]                # 2 credits
numbers = [s["store_number"] for s in nearby["stores"]]
found = client.walgreens.search("shampoo", sort="top_sellers", store_id=numbers[0])["data"]
p = found["products"][0]
print(p["product_id"], p["price"], p["sale_price"], p["availability"]["text"])

stock = client.walgreens.stock(p["product_id"], numbers)["data"]              # 4 credits
for s in stock["stores"]:
    print(s["store_number"], s["status"], s["quantity"], s["in_stock"])
print("unknown:", stock["unknown_store_ids"])

# --- CVS: there is no store locator; the store number is on every cvs.com
# store page ("Store ID: #7019"). search defaults to store 7019 (New York).
found = client.cvs.search("toothpaste", store_id="7019")["data"]
for p in found["products"]:
    print(p["sku_id"], p["price"], p["sale_price"], p["stock"]["in_store"], p["stock"]["pickup"])

# product() can take 10-30+ seconds; the SDK raises its timeout to 120s for it.
item = client.cvs.product(product_id="832677")["data"]
print(item["upc"], item["promo"], item["promo_end_date"], [v["sku_id"] for v in item["variants"]])

units = client.cvs.stock(["832677", "789787"], "7019")["data"]                 # up to 20 SKUs
for i in units["items"]:
    print(i["sku_id"], i["in_store"], i["pickup"], i["ship"])
```

Walgreens and CVS cover retail (front-store) products, not the pharmacy. An
unknown CVS SKU or store number reads as 0 units rather than an error.

### 26. US Retail -- Whole Foods Market, Harbor Freight, PetSmart, Petco, iHerb, Chewy and Menards

Seven more US retailers. Whole Foods prices are per store; Harbor Freight,
PetSmart, Petco, iHerb and Chewy prices are national; Menards prices carry the
mail-in rebate. Every method costs 1 credit except iHerb (2 each), Chewy (10
each) and Menards `product` with a `store_id` (2).

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Whole Foods Market: prices are one store's (5-digit store_id, default 10145,
# Lamar in Austin TX): regular, sale and Prime member price. No per-store stock.
store = client.whole_foods.stores("10019")["data"]["stores"][0]
milk = client.whole_foods.search("milk", store_id=store["store_id"], sort="price_asc")["data"]
for p in milk["products"]:
    print(p["asin"], p["regular_price"], p["sale_price"], p["prime_price"], p["price_unit"], p["name"])

deals = client.whole_foods.deals(store_id=store["store_id"], category="cheese")["data"]
item = client.whole_foods.product(asin="B078WVT2BC", store_id=store["store_id"])["data"]
print(item["in_store"]["regular_price"], item["online"]["price"], item["online"]["availability"])

flyer = client.whole_foods.sales_flyer(store["store_id"])["data"]
for promo in flyer["promotions"]:
    print(promo["headline"], promo["sale_price"], promo["prime_price"], promo["end_date"], promo["asins"])

# --- Harbor Freight: national prices with sale, public coupon, Inside Track Club
# member price and the competitor price it quotes (compare_at).
prices = client.harbor_freight.prices(["73216", "59716"])["data"]
for p in prices["products"]:
    print(p["sku"], p["price"], p["regular_price"], p["sale"], p["coupon"], p["member_deal"], p["compare_at"])

found = client.harbor_freight.search(query="cordless drill")["data"]
print(found["redirect"])                       # set when a keyword maps to a category page
drills = client.harbor_freight.search(category_id="1827", sort="price_low")["data"]

# Stock is a status (in_stock, limited, out_of_stock, not_carried) plus the
# aisle, from a daily snapshot -- not a unit count.
stock = client.harbor_freight.availability(["73216"], zip="90012", limit=5)["data"]
print(stock["inventory_updated_at"])
for s in stock["stores"]:
    for i in s["items"]:
        print(s["store_id"], s["name"], i["sku"], i["stock_status"], i["aisle"])

# --- PetSmart: national prices with the Autoship first-order and recurring
# price; stock is a unit count per store.
found = client.petsmart.search("dog food", store_id="1658")["data"]   # in stock at that store
p = found["products"][0]
item = client.petsmart.product(web_style_id=p["web_style_id"])["data"]
for v in item["variants"]:
    print(v["sku"], v["options"], v["price"], v["sale_price"], v["autoship"])  # autoship: first_order_price, recurring_price

stock = client.petsmart.store_stock("1658", [v["sku"] for v in item["variants"]])["data"]
for i in stock["items"]:
    print(i["sku"], i["store_quantity"], i["ship_to_home_quantity"])
pairs = client.petsmart.availability([{"store_id": "1658", "sku": "5252900"}, {"store_id": "2528", "sku": "5252900"}])
sale = client.petsmart.deals(pet="dog")["data"]
print([p["name"] for p in sale["products"] if p["on_sale"]])   # the Sale section also lists non-price promotions

# --- Petco: national price plus the Repeat Delivery (autoship) price. Store
# inventory takes cat_entry_id (from search or product), not the part number.
found = client.petco.search("dog food")["data"]
p = found["products"][0]
print(p["part_number"], p["cat_entry_id"], p["price"], p["list_price"], p["autoship_price"])

# Petco calls can take 10-30 seconds; the SDK raises their timeout to 120s.
item = client.petco.product(url=p["url"])["data"]
for v in item["variants"]:
    print(v["cat_entry_id"], v["price"], v["autoship_price"], v["first_autoship_price"], v["online_quantity"])

store = client.petco.stores("10001", limit=1)["data"]["stores"][0]
inv = client.petco.store_inventory([v["cat_entry_id"] for v in item["variants"]], store_id=store["store_id"])["data"]
for i in inv["items"]:
    print(i["cat_entry_id"], i["qty_available"], i["alert_level"], i["in_stock"])

# --- iHerb: online only (no stores), US store in USD. 2 credits per call.
# search() and product() can take 10-25 seconds; the SDK raises their timeout to 120s.
found = client.iherb.search("vitamin d", sort="best_selling")["data"]
ids = [p["product_id"] for p in found["products"][:10]]
for row in client.iherb.prices(ids)["data"]["products"]:          # up to 50 ids
    print(row["product_id"], row["found"], row["price"], row["list_price"], row["in_stock"])

summary = client.iherb.reviews(product_id=ids[0])["data"]        # summary, not a review list
print(summary["average_rating"], summary["rating_histogram"]["five"], summary["top_positive_review"])

# --- Chewy: one-time vs Autoship vs first-Autoship price, MAP fields. 10 credits per call.
found = client.chewy.search(query="kong classic dog toy", sort="bestselling")["data"]
print(found["redirect"])                       # set when Chewy sends the query to a category
item = client.chewy.product(product_id=found["products"][0]["product_id"])["data"]
print(item["price"], item["autoship_price"], item["first_autoship_price"], item["map_price"], item["map_enforced"])

# --- Menards: search one store (2 credits), then open a product. Prices carry
# the mail-in rebate and the final price after it. product's store_id adds that
# store's stock and aisle, costs 2 credits and can take 10-40 seconds (timeout
# raised to 120s).
store = client.menards.stores(zip="55401")["data"]["stores"][0]
hits = client.menards.search("sledge hammer", store["store_id"], sort="price_asc")["data"]
print(hits["total_results"], [(p["name"], p["final_price"], p["stock_quantity"]) for p in hits["products"][:3]])
item = client.menards.product(item_id=hits["products"][0]["item_id"], store_id=store["store_id"])["data"]
print(item["everyday_price"], item["sale_price"], item["rebates"], item["final_price"], item["you_save"])
print(item["store"]["stock_quantity"], item["store"]["locations"])
```

Whole Foods returns no ratings, reviews or UPCs. iHerb and Chewy have no store
endpoints. A Petco `store_inventory` call with one unknown `cat_entry_id` is a
404 for the whole batch.

### 27. US Retail -- Nordstrom

nordstrom.com (US site only). `search`, `category` and `brand` return 24
products a page with current and original price ranges, percent off and
on-sale flag (`category` and `brand` add the filter sidebar with product
counts); `product` lists every color and size as a sku with UPC, price, price
type and the quantity available to ship; `reviews` pages a product's full
review history with sort and filters; `availability` adds the stores that can
do in-store pickup per sku; `stores` is the store locator; `suggestions` is
the search-box autocomplete. 5 credits per call, `availability` and `reviews`
10. Every call can take several seconds, so the SDK raises their request
timeout to 120s; `reviews` takes 20-60s (up to about 100s at 200 reviews), so
its floor is 150s.

```python
from scavio import ScavioClient

client = ScavioClient()

# --- Search, deepest markdowns first. sort: relevance (default), rating,
# price_high, price_low, newest, percent_off.
found = client.nordstrom.search("dress", sort="percent_off")["data"]
print(found["total_results"], found["page_count"], found["count"])
for p in found["products"][:5]:
    print(p["style_id"], p["brand"], p["name"], p["price"], p["original_price_range"], p["percent_off"], p["badges"])

# --- A category (/browse path or URL, incl. sale/women and /browse/new) or a
# brand page: same product rows plus breadcrumbs, subcategories and filters.
cat = client.nordstrom.category("/browse/women/clothing/dresses", sort="price_low")["data"]
print(cat["category"]["title"], cat["total_results"], [s["path"] for s in cat["category"]["subcategories"][:3]])
for f in cat["filters"][:3]:
    print(f["name"], f["option_count"], [(o["label"], o["count"]) for o in f["options"][:3]])
brand = client.nordstrom.brand("/brands/astr-the-label--53360")["data"]
print(brand["brand"]["name"], brand["total_results"])

# --- One product by url or style_id: per-size UPC, price and online stock.
item = client.nordstrom.product(style_id="7737947")["data"]
print(item["price_range"], item["clearance_price_range"], item["rating"], item["review_count"])
for color in item["colors"]:
    for sku in color["skus"]:
        print(color["name"], sku["size"], sku["upc"], sku["price"], sku["price_type"], sku["in_stock"], sku["quantity"])
print(item["size_fit"]["average"], item["rating_histogram"])
for r in item["reviews"]:
    print(r["rating"], r["size_rating"], r["title"], r["verified_purchase"])

# --- Full review history (10 credits): up to 200 per call, default 60.
# sort: most_helpful (default), most_recent, highest_rated, lowest_rated.
# Filters: stars, verified_only, with_photos, search (not combinable with sort).
rev = client.nordstrom.reviews(style_id="7737947", sort="most_recent", max_reviews=100)["data"]
s = rev["summary"]
print(s["average_rating"], s["total_reviews"], s["ratings_histogram"], s["size_rating"], s["ratings_only_count"])
print([(f["name"], f["mentions"], f["quote"]) for f in s["best_features"][:3]], rev["ai_summary"])
print(rev["total_results"], rev["returned"], rev["has_more"])
for r in rev["reviews"][:5]:
    print(r["date"], r["rating"], r["title"], r["text"], r["size_purchased"], r["helpful_votes"], r["badges"], len(r["photos"]))
critical = client.nordstrom.reviews(style_id="7737947", stars=[1, 2], verified_only=True)["data"]
print(critical["total_results"], [r["text"] for r in critical["reviews"][:3]])

# --- Ship and pickup availability per sku, with the pickup stores (10 credits).
avail = client.nordstrom.availability(style_id="7737947")["data"]
print(avail["sku_count"], avail["in_stock_count"], avail["pickup_store_count"])
for sku in avail["skus"][:3]:
    print(sku["size"], sku["color"], sku["ship_quantity"], sku["pick_quantity"], [s["name"] for s in sku["pickup_stores"]])

# --- Stores near a ZIP (or latitude/longitude, or store_numbers), up to 100 miles.
for store in client.nordstrom.stores(zip="10001")["data"]["stores"][:3]:
    print(store["store_number"], store["name"], store["type"], store["distance_miles"], store["hours"], store["curbside_pickup"])

# --- Autocomplete.
print(client.nordstrom.suggestions("nike air")["data"]["suggestions"])
```

`product` reviews are the ones shown on the product page (up to about 13),
alongside the total `review_count` and `rating_histogram`; `reviews()` returns
the rest. Rating-only reviews come back with `title` and `text` null. If the
upstream page still fails after the API's own retries, the call is an unbilled
502. `quantity` and `ship_quantity` are units available to ship online;
`in_stock` is true when a sku can be shipped or picked up, so a store-only sku
reads in stock with quantity 0. `pick_quantity` is chain-wide: per store
Nordstrom only says whether pickup is available, not how many. A ZIP with no
store in range returns an empty list (billed). An unknown style id, sku id,
category or brand is a 404. For nordstromrack.com use `client.nordstrom_rack`
(next section).

### 28. US Retail -- Nordstrom Rack

nordstromrack.com (US site only), its own namespace `nordstrom_rack`, separate
from `nordstrom` but with the same methods, parameters and credit costs: 5 per
call, `availability` and `reviews` 10. `category` takes Rack's `/shop` and
`/clearance` paths, including Clear the Rack (`/clearance`) and flash events
(`/shop/flash` lists the live events as subcategories, `/shop/flash/event-N`
opens one); there is no `/browse`. `brand` takes `/brands/<slug>` with no id.
Every product row carries `clearance_price_range`, and during Clear the Rack a
clearance item can carry an extra percent off on top: `promotion_price_range`
is the price after it and `promotion_percent_off` the extra percent (all three
are null when not set). `stores` and `availability` cover Rack stores only.
Rack has its own review pool, separate from nordstrom.com's, so the same style
can show a different rating and review count on each. Same timeout floors as
`nordstrom`: 120s, `reviews` 150s (15-60s typical, up to about 100s at 200
reviews).

```python
from scavio import ScavioClient

client = ScavioClient()
rack = client.nordstrom_rack

# --- Clear the Rack: clearance listings, deepest markdowns first.
clr = rack.category("/clearance/women", sort="percent_off")["data"]
print(clr["category"]["title"], clr["total_results"], [s["path"] for s in clr["category"]["subcategories"][:3]])
for p in clr["products"][:5]:
    print(p["style_id"], p["brand"], p["name"], p["price"], p["original_price_range"],
          p["clearance_price_range"], p["promotion_price_range"], p["promotion_percent_off"])

# --- Flash events: /shop/flash lists them, each one is a listing.
events = rack.category("/shop/flash")["data"]["category"]["subcategories"]
print([(e["name"], e["path"]) for e in events[:5]])

# --- Search, a brand page, one product.
found = rack.search("dress", sort="percent_off")["data"]
print(found["total_results"], found["page_count"], found["count"])
brand = rack.brand("/brands/adidas")["data"]
print(brand["brand"]["name"], brand["total_results"])
item = rack.product(style_id="8816500")["data"]
print(item["price_range"], item["original_price_range"], item["percent_off"], item["rating"], item["review_count"])
for color in item["colors"]:
    for sku in color["skus"]:
        print(color["name"], sku["size"], sku["upc"], sku["price"], sku["price_type"], sku["in_stock"], sku["quantity"])

# --- Rack's own reviews (10 credits), same sort and filters as nordstrom.
rev = rack.reviews(style_id="7737947", max_reviews=50)["data"]
print(rev["summary"]["average_rating"], rev["summary"]["total_reviews"], rev["has_more"])

# --- In-store pickup per sku at Rack stores (10 credits), and the store locator.
avail = rack.availability(style_id="7737947")["data"]
for sku in avail["skus"][:3]:
    print(sku["size"], sku["color"], sku["ship_quantity"], sku["pick_quantity"], [s["name"] for s in sku["pickup_stores"]])
for store in rack.stores(zip="10001")["data"]["stores"][:3]:
    print(store["store_number"], store["name"], store["type"], store["distance_miles"])

print(rack.suggestions("dre")["data"]["suggestions"])
```

`pick_quantity` is chain-wide: per store the site only says whether pickup is
available, not how many. Responses carry no event start or end dates. An
unknown style id, sku id, category or brand is a 404.

### 29. US Retail -- Best Buy

bestbuy.com (US site only), namespace `best_buy`, 9 endpoints. Credits:
`search`, `product`, `reviews` and `prices` 2 each (`prices` is per call, up to
15 SKUs); `category` 2 for an `abcat` id and 3 for a `pcmcat` page; `deals` 3;
`stores` and `suggestions` 1; `availability` 2 flat for up to 8 stores.
`product`, `reviews` and `availability` take `sku` or `url`; `availability`
takes exactly one of `zip` or `store_ids`. `filters` is a dict: `brand`,
`on_sale`, `clearance`, `open_box`, and `min_price` with `max_price` (both
bounds). Search and category return 18 organic products per page; sponsored
tiles only with `include_sponsored=True`. Every method raises the request
timeout to at least 120s; `availability` typically takes 5-20s.

```python
from scavio import ScavioClient

client = ScavioClient()
bb = client.best_buy

# --- Search with filters, then a category listing.
found = bb.search("tv", sort="best_selling", filters={"brand": "Samsung", "on_sale": True})["data"]
print(found["total_results"], found["total_pages"], found["count"], found["sponsored_count"])
for p in found["products"][:5]:
    print(p["sku"], p["model"], p["name"], p["price"], p["regular_price"], p["savings_percent"], p["badge"])
tvs = bb.category(category_id="abcat0101001", sort="price_low")["data"]
print(tvs["category"]["name"], tvs["total_results"])

# --- One product: open-box offers by condition, UPC, specs.
item = bb.product(sku="6607832")["data"]
print(item["upc"], item["model"], item["price"], item["regular_price"], item["review_summary"])
for ob in item["open_box"]:
    print(ob["condition"], ob["price"], ob["savings_vs_new"], ob["savings_vs_regular"])

# --- Store pickup status at the stores nearest a ZIP (2 credits flat).
avail = bb.availability(sku="6607832", zip="94103", max_stores=5)["data"]
print(avail["in_stock_count"], avail["status_counts"])
for store in avail["stores"]:
    print(store["store_id"], store["name"], store["status"], store["quantity"], store["pickup_date"])

# --- Up to 15 prices in one call (2 credits), Deal of the Day, reviews.
for row in bb.prices(["6607832", "6673112", "6679316"])["data"]["prices"]:
    print(row["sku"], row["found"], row["price"], row["regular_price"], row["on_sale"])
deals = bb.deals()["data"]
print(deals["deal_of_the_day"]["name"], deals["deal_of_the_day"]["price"], deals["countdown_ends"])
rev = bb.reviews(sku="6607832", sort="newest")["data"]
print(rev["average_rating"], rev["recommended_percent"], [(c["feature"], c["mentions"]) for c in rev["pros"]])

# --- Store locator and autocomplete.
for store in bb.stores("94103")["data"]["stores"][:3]:
    print(store["store_id"], store["name"], store["distance_miles"], store["hours"][0])
print([s["term"] for s in bb.suggestions("ps5 con")["data"]["suggestions"]])
```

Availability is store pickup status, not a unit count: `quantity` is set only
for `limited` (Best Buy's "only N left") and is null for `in_stock`. Statuses
are `in_stock`, `limited`, `ship_to_store`, `out_of_stock`,
`not_available_for_pickup` and `unknown` (with a `reason`). In `prices`, a SKU
Best Buy does not know comes back `found: False`; all unknown is a 404. An
unknown SKU or category is a 404.

### 30. Trading Cards -- TCGplayer

tcgplayer.com (US marketplace, USD), namespace `tcgplayer`, 13 endpoints, 1
credit each: `search`, `product`, `listings`, `price_history`, `sales`,
`games`, `sets`, `price_guide`, `suggestions`, `trending`, `seller`,
`seller_feedback`, `seller_products`. Covers every game TCGplayer lists
(Pokemon, Magic: The Gathering, Yu-Gi-Oh!, One Piece, Lorcana and 60+ more).
`product`, `listings`, `price_history` and `sales` take `product_id` or a
tcgplayer.com `/product/<id>/` `url`. `search` needs a query unless `game` or
`set` is given. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
tcg = client.tcgplayer

# --- Search a game, then one product with market price per SKU.
found = tcg.search("charizard", game="pokemon", sort="price_desc", limit=10)["data"]
print(found["total_results"], found["count"], found["has_more"])
for p in found["products"][:5]:
    print(p["product_id"], p["name"], p["set_name"], p["market_price"], p["listing_count"])

card = tcg.product(product_id=219058)["data"]
print(card["name"], card["market_price"], card["median_price"], card["seller_count"])
for sku in card["skus"]:
    # lowest/highest_sale_price and sale_count are recent SALE stats, not listings.
    print(sku["condition"], sku["printing"], sku["language"], sku["market_price"],
          sku["lowest_sale_price"], sku["highest_sale_price"], sku["sale_count"])

# --- Live offers, cheapest price plus shipping first.
offers = tcg.listings(product_id=219058, condition=["Near Mint"], limit=10)["data"]
for row in offers["listings"]:
    s = row["seller"]
    print(row["price"], row["shipping_price"], row["condition"], s["name"], s["rating_percent"])

# --- Sold volume over a month (daily buckets) and the 5 newest sales.
hist = tcg.price_history(product_id=219058, range="month")["data"]
print(hist["totals"]["quantity_sold"], hist["totals"]["transaction_count"])
for b in hist["skus"][0]["buckets"][:7]:
    print(b["date"], b["market_price"], b["quantity_sold"], b["low_sale_price"])
for sale in tcg.sales(product_id=219058)["data"]["sales"]:
    print(sale["date"], sale["condition"], sale["price"], sale["shipping_price"])

# --- Games -> sets -> a whole set's price guide.
games = tcg.games()["data"]["games"]
sets = tcg.sets("pokemon")["data"]["sets"]
guide = tcg.price_guide(604, limit=500)["data"]
print(len(games), sets[0]["set_id"], guide["set_name"], guide["total_results"])
for row in guide["rows"][:5]:
    print(row["name"], row["number"], row["condition"], row["market_price"], row["low_price"])

# --- Autocomplete, trending searches, and sellers.
print([p["name"] for p in tcg.suggestions("charizard")["data"]["products"]])
print([t["term"] for t in tcg.trending(game="pokemon")["data"]["terms"]])
seller = tcg.seller("58f7acae")["data"]
print(seller["name"], seller["rating_percent"], seller["feedback"]["total"])
fb = tcg.seller_feedback("58f7acae", rating=1, with_comment=True)["data"]
stock = tcg.seller_products("58f7acae", game="pokemon")["data"]
print(fb["total_results"], stock["total_results"])
```

`sales` returns only the 5 most recent sales (TCGplayer shows no more); use
`price_history` for sold volume, where `low_sale_price` and `high_sale_price`
are null in a bucket with no sales. Buckets are daily for `month`, 3-day for
`quarter` (default) and weekly for `semi_annual` and `annual`. Seller methods
take the 8-character `seller.key` from a listing; feedback buyers appear only
as the site's masked nickname. An unknown product id, game, set or seller key
is a 404. No store locator, product reviews or buylist prices.

### 31. Second-hand Fashion -- Vinted

Vinted on 27 country sites, namespace `vinted`, 9 endpoints, 1 credit each:
`search`, `product`, `seller`, `seller_products`, `seller_feedback`, `brands`,
`suggestions`, `filters`, `categories`. Every method takes an optional
`country`: `fr` (default), `be`, `lu`, `es`, `nl`, `lt`, `de`, `at`, `it`,
`uk`, `pt`, `us`, `cz`, `sk`, `pl`, `se`, `ro`, `hu`, `dk`, `fi`, `hr`, `gr`,
`ie`, `ee`, `lv`, `si`, `au`. Category, condition and filter names come back in
that site's language. `product` takes `item_id` or a Vinted item `url` (the
URL's own site wins). Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
v = client.vinted

# --- Search one country site; price is in that site's currency.
found = v.search("barbour jacket", country="uk")["data"]
print(found["listed_results"], found["total_pages"], found["total_is_capped"])
for item in found["items"][:5]:
    # service_fee is the Vinted fee the buyer pays on top of price.
    print(item["id"], item["title"], item["price"], item["currency"],
          item["service_fee"], item["total_price"], item["condition"], item["seller"]["id"])

# --- Resolve ids for filters: brands, conditions/sizes/colors, categories.
brand = v.brands("barbour", country="uk")["data"]["brands"][0]
print(brand["id"], brand["title"], brand["item_count"], brand["is_luxury"])
for opt in v.filters("status", country="uk")["data"]["options"]:
    print(opt["id"], opt["title"], opt["item_count"])
tree = v.categories(country="uk", parent_id=1904)["data"]
print(tree["parent"]["title"], [c["title"] for c in tree["categories"]][:5])
print([s["text"] for s in v.suggestions("barb", country="uk")["data"]["suggestions"]])

# --- One listing, priced in the SELLER's currency.
item = v.product(url="https://www.vinted.co.uk/items/10671938315-nike-air-max-size-uk-75")["data"]
print(item["title"], item["price"], item["currency"], item["condition"], item["is_sold"])
print(item["category"]["path"][-1]["title"], item["seller"]["login"],
      item["seller"]["feedback_reputation"])

# --- A seller: public profile, listings and reviews.
seller = v.seller(65958245, country="uk")["data"]
print(seller["login"], seller["feedback_count"], seller["feedback_reputation"], seller["item_count"])
wardrobe = v.seller_products(65958245, country="uk", limit=10)["data"]
reviews = v.seller_feedback(65958245, country="uk")["data"]
print(wardrobe["total_results"], reviews["total_results"])
for fb in reviews["feedback"][:3]:
    print(fb["rating"], fb["created_at"], fb["is_automatic"], fb["text"])
```

Every site, `uk` (GBP), `us` (USD) and `au` (AUD) included, can show listings
from sellers in other countries, with the price converted to the site's
currency (EUR, or CZK, PLN, SEK, RON, HUF, DKK on the other sites); the EU sites
share one cross-border pool. `product` returns the seller's own price and
currency, which can differ from the site's. `search` returns 96 items per page and Vinted
serves at most 10 pages (`total_is_capped` is true past 960 matches); price
sorts also surface loosely matching cheap listings, so pair them with a
category or price range. `search`'s `filters` echoes what Vinted actually
applied. Live listings only: there is no sold-item search, shipping price,
pickup point or similar-items endpoint. Seller data is limited to public,
buyer-relevant fields and feedback carries no reviewer identity. An unknown
item or member id on `product` or `seller` is a 404.

### 32. Department Store -- Macy's

macys.com (US, USD), namespace `macys`, 9 endpoints, 1 credit each: `search`,
`product`, `reviews`, `category`, `brand`, `deals`, `stores`,
`store_availability`, `suggestions`. No `country`: the US site only. `product`,
`reviews` and `store_availability` take `product_id` or a macys.com product
`url`; `category` takes `category_id` or `url`; `brand` takes `brand_id` (a
product's `brand_page_id`) or `url`. Every method raises the request timeout to
at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
m = client.macys

# --- Search: 60 organic items per page, filters from the facets.
found = m.search("jeans", brand="Levi's", special_offer="clearance", sort="price_low_to_high")["data"]
print(found["total"], found["total_pages"], found["sponsored_dropped"])
for item in found["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["percent_off"], item["sale_ends"], item["deal_label"], item["is_sponsored"])
for facet in found["facets"][:3]:
    print(facet["name"], [(v["value"], v["count"]) for v in facet["values"][:3]])

# --- Deals: sale, clearance, today_only, last_act, limited_time_special, black_friday.
clearance = m.deals(type="clearance", filters={"GENDER": "Women"})["data"]
print(clearance["label"], clearance["total"])

# --- One product (or up to 10 with product_ids, summary view).
p = m.product(product_id=25822310)["data"]
print(p["title"], p["price"], p["regular_price"], p["on_sale"], p["sale_ends"])
print(p["review_count"], p["text_review_count"], p["rating_distribution"])
for v in p["variants"][:3]:
    print(v["upc"], v["color"], v["size"], v["available"], v["availability_message"])

# --- Written reviews only (ratings without text are counted on product).
for r in m.reviews(product_id=25822310, sort="lowest_rated", limit=20)["data"]["reviews"]:
    print(r["rating"], r["date"], r["nickname"], r["title"], r["text"][:80])

# --- Store pickup: stores near a ZIP, then per-variant flags at one store.
stores = m.stores(zip="10001")["data"]["stores"]
store_id = stores[0]["store_id"]
at_store = m.store_availability(product_id=25822310, store_id=store_id)["data"]
print(at_store["pickup_available_count"], at_store["in_store_available_count"])
for v in at_store["variants"][:3]:
    print(v["upc"], v["color"], v["size"], v["pickup_available"], v["in_store_available"])
print(m.suggestions("jea")["data"]["suggestions"])
```

`search`, `category`, `brand` and `deals` share one grid: 60 organic items per
page with `total` and `total_pages`, and totals can differ between sorts, as
they do on the site. Any facet value from `facets` works in `filters`, and
`brand`, `color`, `special_offer`, `min_price` / `max_price` and
`pickup_store_id` are first-class arguments. Ad-only sponsored tiles are
dropped (`sponsored_dropped` counts them) unless `include_sponsored=True`;
organic items that also hold a paid slot stay, flagged `is_sponsored`. A
keyword Macy's maps to a category comes back with `redirected_to_category`.
A `product_ids` batch (up to 10) gets Macy's summary view: no rating histogram,
and a collection without its members' variants; a collection member's id
answers with the collection product (`requested_id` echoes the id asked for).
`review_count` includes ratings without text, `reviews` returns written reviews
only. `store_availability` takes a `store_id` (per-variant `pickup_available`
and `in_store_available`) or a location (`zip`, `lat` + `lng`, or `city` +
`state`: which stores can hand the product over), not both. Macy's publishes
no unit quantities, so there are no stock counts. No coupon codes, Q&A text or
price history: to track prices, poll and store your own.

### 33. Department Store -- Saks Fifth Avenue

saksfifthavenue.com (US, USD), namespace `saks`, 9 endpoints, 2 credits each:
`search`, `product`, `category`, `brand`, `deals`, `stores`,
`store_availability`, `suggestions`, `designers`. No `country`: the US site
only. `product` takes `product_id` (master or variant) or a product `url`;
`category` takes a `/c/` `path` or `url`; `brand` takes a designer slug (from
`designers`) or `url`; `stores` and `store_availability` take `zip` or `lat` +
`lng`. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
s = client.saks

# --- Designer sale: 24 grid positions per page, filters from the facets.
sale = s.deals(type="womens_sale", brand="Prada", sort="price_low_to_high")["data"]
print(sale["label"], sale["total"], sale["total_pages"], sale["next_start"])
for item in sale["items"][:5]:
    print(item["id"], item["brand"], item["title"], item["price"],
          item["regular_price"], item["percent_off"], item["badge"])
for facet in sale["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])

# --- Walk every item: pass next_start back as start (editorial tiles can take a slot).
more = s.deals(type="womens_sale", brand="Prada", sort="price_low_to_high",
               start=sale["next_start"])["data"]
print(more["start"], more["count"], more["next_start"])

# --- Search: size takes the facet label ("Medium", not "M").
found = s.search("coat", size="Medium", on_sale=True)["data"]
print(found["total"], found["redirected_to"])

# --- One product, then one variant's pickup stock near a ZIP.
p = s.product(product_id="0400019127312")["data"]
print(p["title"], p["price"], p["on_sale"], p["is_final_sale"], p["rating"], p["review_count"])
for v in p["variants"][:3]:
    print(v["sku"], v["warehouse_units"])
near = s.store_availability(p["variants"][0]["sku"], zip="10022")["data"]
for st in near["stores"]:
    print(st["name"], st["availability_message"], st["in_stock"], st["units_at_store"])

# --- Designer index: slugs feed brand().
for d in s.designers(letter="G")["data"]["designers"][:5]:
    print(d["name"], d["slug"])
print(s.brand(brand="gucci", new_arrivals=True)["data"]["total"])
```

`search`, `category`, `brand` and `deals` share one grid: 24 positions per
page with `total`, `total_pages`, `start` and `next_start`. An editorial tile
can take a grid position, so a page may carry 22-23 items: pass the previous
`next_start` as `start` to miss nothing (`page` also works). Any facet value
from `facets` works in `filters`; `brand`, `color`, `size`, `min_price` /
`max_price`, `on_sale` and `new_arrivals` are first-class arguments, and
`size` takes the facet label ("Medium", not "M"). A keyword the site maps to a
designer or category page comes back with `redirected_to`. `deals` lists
`sale`, `womens_sale`, `mens_sale`, `womens_new_arrivals` and
`mens_new_arrivals`; Saks has no clearance or final-sale list (items carry
`is_clearance` / `is_final_sale` flags). `store_availability` needs a VARIANT
sku (a product's `variants[].sku`, or a product resolved with `color` +
`size`) and returns `units_at_store` only when the site shows a count,
otherwise null. Rating and review count only: review text is not available.
No coupon codes, international prices or price history: to track designer
sale prices, poll and store your own.

### 34. Department Store -- Kohl's

kohls.com (US, USD), namespace `kohls`, 9 endpoints, 2 credits each except
`stores` (1 credit): `search`, `product`, `category`, `brand`, `deals`,
`stores`, `store_availability`, `suggestions`, `coupons`. No `country`: the
US site only. `product` takes `product_id` or a product `url` (plus an
optional `store_id`); `category` takes a catalog `path` or `url` that carries
its `CN=` filter; `brand` takes a brand name or `url`; `stores` takes `zip`,
`city` + `state`, or `lat` + `lng`; `store_availability` takes a `sku` and a
`zip`. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
k = client.kohls

# --- Clearance: 120 products per page, sponsored items kept and flagged.
clr = k.deals(type="clearance", sort="percent_off")["data"]
print(clr["label"], clr["total"], clr["total_pages"], clr["sponsored_count"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["price_label"], item["percent_off"], item["with_code_price"],
          item["with_code_offer_codes"], item["is_sponsored"])

# --- Facet value ids feed filters (price is a bucket, not a free min / max).
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = k.search("jeans", brand="Levi's", filters=["Gender:Womens", "Price:$25 to $50"])["data"]
print(found["total"], found["corrected_query"])

# --- One product, then one variant's pickup units near a ZIP.
p = k.product(product_id="6251213")["data"]
print(p["title"], p["price"], p["regular_price"], p["rating"], p["review_count"], p["dept"])
print(p["kohls_cash"], [(o["code"], o["ends"]) for o in p["offers"]])
v = p["variants"][0]
print(v["sku"], v["upc"], v["color"], v["size"], v["online_units"])
near = k.store_availability(v["sku"], "10001", dept=p["dept"])["data"]
print(near["in_stock_count"], near["total_pickup_units"])
for st in near["stores"][:5]:
    print(st["name"], st["pickup_units"], st["stock_level"], st["distance_miles"])

# --- Stores, then today's public coupon codes.
for st in k.stores(zip="60601")["data"]["stores"][:3]:
    print(st["store_id"], st["name"], st["city"], st["badges"])
for c in k.coupons()["data"]["offers"]:
    print(c["code"], c["description"], c["ends"], c["requires_kohls_card"])
```

`search`, `category`, `brand` and `deals` share one grid: 120 products per
page with `total` and `total_pages`. Up to about 8 sponsored items stay in the
list, flagged `is_sponsored` and counted in `sponsored_count`. Any facet value
id from `facets` works in `filters` (one id or a list, combined with AND);
`brand`, `color`, `size`, `on_sale` and `clearance` are first-class
arguments. Price is a facet bucket ("Price:$25 to $50"), not a free min /
max. Search returns `corrected_query` when the site autocorrects a keyword.
`deals` lists `clearance` (default), `sale`, `kohls_cash` (items that earn
Kohl's Cash now) and `sephora` (Sephora at Kohl's). Prices carry
`price_label` (sale, clearance, clearance+regular), `percent_off`,
`with_code_price` (the price after a public offer code, with the code) and
`price_suppressed` + `price_note` for cart-only prices. `store_availability`
takes a product's `variants[].sku` (and optionally its `dept`) and returns
real pickup unit counts at every store within about 50 miles of the ZIP.
Rating and review count only: review text is not available. No price
history, international sites, account offers or checkout: to track
clearance prices, poll and store your own.

### 35. Department Store -- JCPenney

jcpenney.com (US incl. Puerto Rico stores, USD), namespace `jcpenney`, 11
endpoints, 1 credit each: `search`, `product`, `category`, `brand`, `deals`,
`stores`, `store_availability`, `suggestions`, `coupons`, `reviews`,
`questions`. No `country`: the US site only. `product` takes `product_id`, a product `url` or up to 20
`product_ids`; `category` takes a `/g/` `path` or `url` that carries its
`id=cat...`; `brand` takes a brand name or `url`; `stores` takes `zip`,
`city` + `state`, or `lat` + `lng`; `store_availability` takes a `sku` plus
`zip` (or `lat` + `lng`); `reviews` and `questions` take `product_id` or a
product `url`. Every method raises the request timeout to at least 120s;
`reviews` and `questions` raise it to 240s.

```python
from scavio import ScavioClient

client = ScavioClient()
j = client.jcpenney

# --- Clearance: 48 products per page, at most 25 pages.
clr = j.deals(type="clearance")["data"]
print(clr["type"], clr["total"], clr["total_pages"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["price_max"],
          item["regular_price"], item["price_type"], item["percent_off"],
          item["coupon_price"], item["coupon_code"])

# --- Facet values feed filters as {facet id: value}.
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = j.search("jeans", brand="levi's", filters={"gender": "women"})["data"]
print(found["total"], found["corrected_query"], found["redirected_to"])

# --- One product (product-level price ranges), then one variant's units
# --- at the 5 nearest stores.
p = j.product(product_id="ppr5008604049")["data"]
price = p["price"]
print(p["title"], price["current_min"], price["current_max"], price["regular_min"],
      price["price_type"], price["coupon"], p["rating"], p["review_count"])
v = p["variants"][0]
print(v["sku"], v["upc"], v["color"], v["size"], v["online_stock"])
near = j.store_availability(v["sku"], zip="90012")["data"]
print(near["stores_with_stock"], near["total_quantity"])
for st in near["stores"]:
    print(st["name"], st["quantity"], st["status"], st["distance_miles"])

# --- Stores, then today's public coupon codes.
for st in j.stores(zip="75024")["data"]["stores"][:3]:
    print(st["store_id"], st["name"], st["city"], st["services"])
for c in j.coupons()["data"]["coupons"]:
    print(c["code"], c["channel"], c["headline"], c["ends_at"])

# --- Review text (slow: usually 15-90s, up to about 3 minutes).
rv = j.reviews(product_id="ppr5008604049", sort="most_helpful")["data"]
print(rv["total_reviews"], rv["displayed_reviews"], rv["matching_reviews"],
      rv["average_rating"], rv["rating_distribution"], rv["recommended_percent"])
for r in rv["reviews"][:3]:
    print(r["rating"], r["title"], r["author"], r["submitted_at"],
          r["helpful_votes"], r["verified_purchaser"], r["incentivized"], r["syndicated"])

# --- Questions and every answer, with who answered.
qa = j.questions(product_id="ppr5008212471")["data"]
print(qa["total_questions"], qa["total_answers"])
for q in qa["questions"][:3]:
    print(q["question"], q["answer_count"])
    for a in q["answers"]:
        print("  ", a["author_type"], a["ai_label"], a["text"][:80])
```

`search`, `category`, `brand` and `deals` share one grid: 48 products per
page, at most 25 pages (1,200 items deep), with `total` and `total_pages`.
Any facet from `facets` works in `filters` as `{facets[].id: value}` (one
value or a list, facets combined with AND); `brand`, `color`, `size`,
`price_range` and `deal` (a Deals & Promotions label) are first-class
arguments, each one value or a list. Search returns `corrected_query` when
the site autocorrects a keyword and `redirected_to` when it sends a keyword
(doorbusters) to a deal or category listing; `exact=True` skips the
automatic category narrowing. `deals` lists `clearance` (default), `sale`,
`black_friday`, `big_buy`, `limited_time_special`, `best_value`,
`gotta_have_it`, `closeout` and `bogo`, or any `label` verbatim, across all
products or one `department`. Prices are product-level ranges (regular,
sale and clearance min / max, `percent_off`, `price_type`) plus the
after-coupon price and its code: JCPenney does not expose a price per size
or color. Variants carry an online stock level (high / low / out), not a
count. `store_availability` takes a product's `variants[].sku` and returns
real unit counts at the 5 nearest stores. `reviews` returns up to 98 review
texts (default 38), sorted `most_recent` (default), `most_helpful`,
`highest_rating`, `lowest_rating` or `relevance`, optionally one star
`rating`; `total_reviews` counts every language, `displayed_reviews` the
English reviews JCPenney lists, `matching_reviews` those under the sort and
filter. Each review carries `verified_purchaser`, `incentivized`,
`syndicated` with `syndication_source`, photos, videos, secondary ratings
(Quality, Value...) and the brand's response. `questions` returns up to 50
questions (default 10, no sort option) with every answer's `author_type`
(`brand`, `retailer` for JCPenney staff, `ai`, `customer`) and `ai_label`
(AI-Generated / AI-Assisted). Both are slower than the other endpoints
(usually 15-90s, up to about 3 minutes) and failed calls are not charged.
Reviewer age, gender and IP addresses are never returned. No price history,
international sites, account offers or JCPenney Rewards balances, or
checkout: to track clearance prices, poll and store your own.

### 36. Sporting Goods -- Dick's Sporting Goods

dickssportinggoods.com (US, USD), namespace `dicks`, 9 endpoints, 1 credit
each except `product` and `reviews` (2 credits): `search`, `product`,
`products`, `reviews`, `category`, `brand`, `deals`, `store_availability`,
`suggestions`. No `country`: the US site only. `product` and `reviews` take
`product_id` or a product `url`; `products` takes up to 5 `product_ids`;
`category` takes a `/f/` or `/c/` `path`, a `url` or a `category_id`;
`store_availability` takes a list of `skus` plus `zip` (or `lat` + `lng`).
Every method raises the request timeout to at least 120s; `product` and
`reviews` raise it to 240s (usually 20-75s, up to about 2.5 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
d = client.dicks

# --- Clearance: 48 items per page by default, up to 144.
clr = d.deals(type="clearance", sort="savings")["data"]
print(clr["label"], clr["total"], clr["total_pages"])
for item in clr["items"][:5]:
    print(item["id"], item["title"], item["price"], item["price_max"],
          item["list_price"], item["percent_off"], item["is_pinned"],
          item["scheduled_prices"])

# --- Facet values feed filters as {facet id: value}.
for facet in clr["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
found = d.search("running shoes", brand="HOKA", filters={"5495": "Men's"})["data"]
print(found["total"], found["did_you_mean"], found["redirected_to"])

# --- One product: prices differ per SKU (size / color), then store units.
p = d.product(product_id="23FHQMCLFTN9GTXBLMNS")["data"]
print(p["title"], p["price"]["min"], p["price"]["max"], p["is_clearance"])
for v in p["variants"][:5]:
    print(v["sku"], v["color"], v["size"], v["price"], v["list_price"],
          v["is_clearance"], v["online_units"])
skus = [v["sku"] for v in p["variants"][:2]]
near = d.store_availability(skus, zip="60601")["data"]
print(near["stores_with_stock"], near["sku_totals"])
for st in near["stores"][:3]:
    print(st["name"], st["distance_miles"], [(s["sku"], s["units"]) for s in st["skus"]])

# --- The 15 newest reviews plus rating stats.
r = d.reviews(product_id="26UNDMFITN1HRI9WUAETC")["data"]
print(r["stats"]["total"], r["stats"]["average"], r["stats"]["distribution"])
for rev in r["reviews"][:3]:
    print(rev["rating"], rev["title"], rev["submitted_at"])
```

`search`, `category`, `brand` and `deals` share one grid: 48 items per page
by default, up to 144 (`page_size`), with `total` and `total_pages`, sorted
by `relevance`, `top_sellers`, `savings`, `price_low_to_high`,
`price_high_to_low`, `featured`, `new_arrivals` or `brand_az`. Any facet
from `facets` works in `filters` as `{facets[].id: value}` (one value or a
list, facets combined with AND); `min_price` / `max_price` are approximate.
Merchandised items are flagged `is_pinned` and can make page 1 a few items
longer than `page_size`. Search returns `did_you_mean` for a misspelled
query and follows keywords Dick's sends to a landing page (`clearance`,
`golf balls`), reported as `redirected_to`. `scheduled_prices` are the
retailer's own planned offer-price windows and can change: not a forecast
or price history. `deals` lists `clearance` (default), `sale` or
`weekly_deals`. Prices differ per size and color, so `product` lists every
SKU with its own price, list price, `is_clearance`, `online_units`, UPC and
`buyable` flag; `products` is the cheap style-level summary for up to 5
ids. `reviews` returns the 15 newest reviews with full text and the rating
stats: no paging, sort or star filter, and questions and answers are counts
only. `store_availability` takes SKUs from `product` and returns unit counts
at up to 100 DICK'S, Golf Galaxy (`chain="golf_galaxy"`) or Public Lands
(`chain="public_lands"`) stores, with each store's address, phone, hours and
distance; there is no standalone store locator, and an unknown SKU reads 0
everywhere. No price history, ScoreCard prices or points, international
sites, account data or checkout: to track clearance prices, poll and store
your own.

### 37. Sneakers -- Foot Locker

Foot Locker, namespace `footlocker`, 10 endpoints, 1 credit each: `search`,
`product`, `category`, `brand`, `deals`, `releases`, `stores`,
`store_availability`, `reviews`, `questions`. `country` picks the
storefront: `us` (footlocker.com, USD, default), `ca` (CAD, `language` en
or fr), `gb` (GBP), `de`, `fr`, `it`, `es`, `nl`, `be` (`language` nl or
fr), `at`, `ie` (EUR), `au` (AUD) or `nz` (NZD); titles come in the
storefront's language. Search, product, category, brand and deals (`sale`,
`discount_eligible`) work on all 13; `exclusives` on us and ca; `releases`
on us, ca and gb (gb has no prices or reservation windows); `stores`,
`store_availability`, `reviews` and `questions` are US only. Every method
raises the request timeout to at least 120s; `reviews` and `questions`
raise it to 240s (usually 25-90s, up to about 3-4 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
fl = client.footlocker

# --- Search: 48 items per page, any storefront, data_as_of on every listing.
res = fl.search("nike dunk", country="de", sort="price_low_to_high")["data"]
print(res["currency"], res["total"], res["total_pages"], res["data_as_of"], res["redirected_to"])
for item in res["items"][:5]:
    print(item["id"], item["title"], item["price"], item["list_price"],
          item["percent_off"], item["lowest_price_30d"])

# --- Facet values feed filters as {facet id: value}.
for facet in res["facets"][:3]:
    print(facet["id"], facet["label"], [(v["value"], v["count"]) for v in facet["values"][:3]])
mens10 = fl.brand(brand="New Balance", filters={"mensShoesSize": "10.0"})["data"]
print(mens10["brand"], mens10["total"])

# --- One product: availability is yes / no per size, never unit counts.
p = fl.product(product_id="Q5495005")["data"]
print(p["title"], p["price"], p["launch"])
for size in p["sizes"][:5]:
    print(size["size"], size["available"], size["ship"], size["pickup"],
          size["stores_available"])

# --- Which nearby stores show size 10.0 as available (US).
near = fl.store_availability(product_id="W2288111", size="10.0", zip="10001")["data"]
print(near["stores_with_availability"])
for st in near["stores"][:3]:
    print(st["name_secondary"], st["distance_miles"], st["available"], st["sizes_available"])

# --- The release calendar: monitoring data only.
cal = fl.releases(status="upcoming", brand="Jordan")["data"]
for r in cal["releases"][:5]:
    print(r["launch_at"], r["title"], r["style"], r["retail_price"], r["heat_level"],
          r["reservation"]["status"])

# --- Reviews (slow): 1-98 with full text, sort and star filter.
rv = fl.reviews(product_id="Q5495005", sort="most_helpful", limit=30)["data"]
print(rv["stats"]["average_rating"], rv["stats"]["rating_distribution"])
for review in rv["reviews"][:3]:
    print(review["rating"], review["title"], review["submitted_at"])
```

`search`, `category`, `brand` and `deals` share one grid: 48 items per page
with `total` and `total_pages`, sorted by `relevance`, `price_low_to_high`,
`price_high_to_low`, `new_arrivals`, `top_rated`, `name_az` or `brand_az`.
Filter by `brand` (any case), `gender`, `color`, `price_range`, `on_sale`,
or any facet from `facets` via `filters` as `{facets[].id: value}` (one
value or a list, filters combined with AND). Listings can be a few hours
old: `data_as_of` says when each one was built. A bare brand keyword
(`nike`, `hoka`) is answered with that brand's listing and reported as
`redirected_to`; a keyword the site sends to a landing page without a
product listing is an unbilled 400 pointing to `brand`, `category` or
`deals`. `product` lists every colorway with its price and every size with
`available`, `ship`, `pickup` and `stores_available` (how many stores show
the size as available: a store count, not units); European storefronts add
`lowest_price_30d`. `releases` is the release calendar as monitoring data:
launch date and time, retail price, colorway, style code, heat level, size
run and reservation windows where the storefront runs them; nothing here
enters, reserves or buys a release. `store_availability` covers Foot Locker
banner stores only (no Kids Foot Locker or Champs) and answers yes / no.
Unknown SKUs, categories and brands are a charged 404. No search
suggestions, member (FLX) prices or account data, price history or
checkout: to track prices, poll and store your own.

### 38. Fan Merchandise -- Fanatics

Fanatics merchandise and product data (jerseys, hats, fan gear,
collectibles; not sportsbook odds), namespace `fanatics`, 5 endpoints, 1
credit each: `search`, `product`, `browse`, `deals`, `reviews`. `country`
picks the storefront: `us` (fanatics.com, USD, default), `gb` (GBP), `de`,
`fr`, `es`, `it` (EUR), `jp` (JPY) or `ca` (CAD, `language` en or fr);
titles come in the storefront's language. `site` reads a US league store
(with country us): `fanatics` (default), `nflshop`, `mlbshop`, `nhlshop` or
`mlsstore`; the same product ids work on every store, but department and
filter ids are per store (Jerseys is 8011 on fanatics.com, 14012 on NFL
Shop): take them from the facets of the store you query. `search`, `product`,
`browse` and `deals` take both; `reviews` is US only (fanatics.com). Every
method raises the request timeout to at least 120s; `reviews` raises it to
300s (usually 20-90s, up to about 4 minutes).

```python
from scavio import ScavioClient

client = ScavioClient()
fan = client.fanatics

# --- Search: up to 72 items per page, data_as_of on every listing.
res = fan.search("chiefs jersey", sort="price_low_to_high")["data"]
print(res["total"], res["total_capped"], res["corrected_query"], res["data_as_of"])
for item in res["items"][:5]:
    print(item["id"], item["title"], item["price"], item["regular_price"],
          item["with_code_price"], item["price_label"], item["ship_by"])

# --- Facet values feed filters as {filter: value}; ids feed browse().
for facet in res["facets"][:3]:
    print(facet["id"], facet["label"], [(v["label"], v["filter"], v["value"]) for v in facet["values"][:3]])

# --- A team's hats, or a league store (NFL Shop): same product ids, its own department ids.
hats = fan.browse(team_id=3372, department_id=8008, price_band="25_50")["data"]
print(hats["browse"]["team"], hats["browse"]["department"], hats["total"])
nfl = fan.search("mahomes jersey", site="nflshop")["data"]
print(nfl["site"], nfl["total"])

# --- One product: regular / sale / clearance / with-code price, stock level per size.
p = fan.product(product_id="3892922")["data"]
print(p["title"], p["price"], p["sale_price"], p["clearance_price"], p["with_code_price"])
print(p["coupon"], p["flags"], p["customizable"], p["personalization"])
for size in p["sizes"]:
    print(size["size"], size["available"], size["stock_level"], size["ship_by"],
          size["est_delivery_from"], size["est_delivery_to"])

# --- Sale and clearance listings, other storefronts in local currency.
sale = fan.deals(type="clearance", league_id=25)["data"]
print(sale["count"], sale["total"])
de = fan.deals(country="de")["data"]
print(de["currency"], de["total"], de["data_as_of"])

# --- Reviews (slow): style rollup, so each review names its product.
rv = fan.reviews(product_id="3892922", sort="most_recent", limit=30)["data"]
print(rv["stats"]["average"], rv["stats"]["fit"], rv["ai_summary"])
for review in rv["reviews"][:3]:
    print(review["product_id"], review["rating"], review["fit"], review["text"])
```

`search`, `browse` and `deals` share one grid: 24, 48 or 72 items per page
(default 72) with `total`, `total_capped` (the US site counts at most 9000)
and `total_pages`, sorted by `top_sellers`, `price_low_to_high`,
`price_high_to_low` or `newest` (price sorts use the current `price`, before
any promo code, not `with_code_price`). Each item carries `price`,
`regular_price`, `sale_price`, `clearance_price`, `with_code_price` (the
price with the site-wide promo code shown on the page) and `price_label`
(`coupon` means coupon-eligible; a null `with_code_price` means the code does
not lower that item). Player ids come from the players facet when the page
lists one (e.g. Lakers) or from a product's `player`.
Filter by `gender`, ids (`league_id`, `team_id`, `player_id`,
`department_id`, `brand_id`, `collection_id`; `browse` and `deals`) or any
facet value via `filters` as `{filter: value}`, one value per filter;
`price_band` and `on_sale` are on `browse` (price bands are not on jp). A
league alone is a landing page: combine it with another id or a filter.
`data_as_of` says when Fanatics built each listing; misspellings come back
as `corrected_query`. `product` lists every size with `stock_level` (low /
out: a level, never a unit count), ship-by and delivery estimates, the
current promo code, personalization fields with the team roster (prices
already include personalization), and jersey assurance / authentic flags.
`reviews` returns real text with 4 sorts and a star filter (1-50, default
10), fit / quality / value, and the site's own AI-written summary
(`ai_summary`); Fanatics pools reviews across a style, so check each
review's `product_id`. Unknown products are a charged 404. No search
suggestions, store locator or store stock, Q&A, FanCash, member pricing,
unit counts, price history or checkout: to track jersey sale prices, poll
and store your own.

### 39. Grocery -- Carrefour

Carrefour grocery prices by store, promotions, Nutri-Score and stores,
namespace `carrefour`, 9 endpoints, 1 credit each: `search`, `product`,
`reviews`, `category`, `promotions`, `suggestions`, `stores`,
`store_availability`, `store`. carrefour.fr (France) serves every endpoint;
`search` and `product` also take `country` `ar` (Argentina, ARS), `ro`
(Romania, RON) or `be` (Belgium, EUR, `language` fr or nl; 2 credits). Data
comes back in the market's language: French titles, labels and ingredients
on fr. Without `store` a price is carrefour.fr's national online price; pass
a store ref from `stores()` (`store_ref` or `pickup_refs[].ref`) or
`store_availability()` (`stores[].store.ref`) for that store's shelf price
and assortment. Every method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
cf = client.carrefour

# --- Search: national online price, unit price, promotion, Nutri-Score.
res = cf.search("nutella")["data"]
print(res["total"], res["store"], res["price_scope"], res["currency"])
for item in res["items"][:5]:
    print(item["ean"], item["title"], item["price"], item["unit_price_label"],
          item["nutriscore"], item["promotion"])

# --- Stores near a postal code; a store ref scopes prices to that store.
stores = cf.stores(postal_code="69003")["data"]["stores"]
for s in stores[:3]:
    print(s["store_ref"], s["name"], s["banner"], s["distance_km"], s["slug"])
local = cf.search("nutella", store="840093")["data"]
print(local["store"], local["price_scope"], local["total"])

# --- One product: ingredients, allergens, nutrition per 100 g, rating.
p = cf.product(ean="3017620422003")["data"]
print(p["title"], p["price"], p["unit_price"], p["unit"], p["ecoscore"])
print(p["ingredients"], p["allergens"])
for row in p["nutrition"]["per_100"]["values"]:
    print(row["nutrient"], row["quantity"])

# --- Promotions: catalogue, immediate, loyalty-card (member) or festive.
promo = cf.promotions(type="loyalty", category="Boissons")["data"]
for item in promo["items"][:3]:
    d = item["promotion"]
    print(item["title"], d["label"], d["loyalty_only"], d["discounted_price"],
          d["initial_price"], d["ends_at"])

# --- Which nearby stores carry a product (yes / no, no price), store detail with fuel.
av = cf.store_availability("3017620422003", "69003")["data"]
print(av["available_count"], [(s["store"]["ref"], s["available"]) for s in av["stores"][:3]])
st = cf.store(slug="venissieux")["data"]
print(st["store"]["name"], st["store"]["next_slots"])
if st["fuel"]:
    for f in st["fuel"]["prices"]:
        print(f["fuel"], f["price_per_litre"], f["updated_at"])

# --- Verified-purchase reviews, and other markets (search / product only).
rv = cf.reviews("8006530256179", sort="lowest_rated", limit=20)["data"]
print(rv["total"], [(r["author"], r["rating"], r["text"]) for r in rv["reviews"][:2]])
be = cf.search("chocolat", country="be", language="nl")["data"]
print(be["country"], be["language"], be["currency"], be["total"])
```

`search`, `category` and `promotions` share one grid (30 items per page on
fr; ar and ro 24, be 36) with `total`, `total_pages` and every facet; filter
by `brand`, `promotion`, `nutriscore`, `organic`, `carrefour_brands` or
`min_price` / `max_price`, and sort by `relevance`, `price_low_to_high`,
`price_high_to_low`, `unit_price_low_to_high`, `unit_price_high_to_low` or
`top_rated` (ar and ro: relevance and the price sorts; be: relevance). Each
item carries `price`, `unit_price` with `unit_price_label` (per kg / L),
`nutriscore`, `ecoscore` and `promotion` (`type`, `label`, `loyalty_only` for
loyalty-card prices, `discounted_price`, `initial_price`, `quantity`,
`starts_at`, `ends_at`). On multi-buy deals ("Le 2ème à -50%") the prices
cover `quantity` items and `discounted_price` is None when the site does not
price the deal. Store prices differ from national ones (Nutella 400 g: 3.99
national, 3.69 at two stores, 4.61 at another). `reviews` returns 1-50
verified-purchase reviews (default 10) with 4 sorts, a star filter and
`offset` paging; authors appear as published (first name and last initial).
`stores` finds stores by postal code or `lat` / `lng`, optionally with one
`service` (`drive`, `station_service`...). `store` returns services, weekly
hours, drive hours, the next pickup slots as shown and, at stores with a fuel
station, fuel prices per litre with update times. Failed calls are not
charged; a not-found is a charged 404. No Q&A, printed leaflet,
delivery-slot booking, cart, loyalty account data or price history: to track
prices, poll and store your own. Spain, Italy, Poland, Brazil and the Middle
East sites are not covered.

### 40. Marketplace -- Allegro

Allegro offers, every seller's price for one product, sellers and seller
feedback, namespace `allegro`, 7 endpoints, 2 credits each: `search`,
`offer`, `product`, `product_offers`, `seller`, `seller_feedback`,
`category`. Every endpoint takes `country`: `pl` (allegro.pl, PLN, default),
`cz` (allegro.cz, CZK), `sk` (allegro.sk, EUR) or `hu` (allegro.hu, HUF).
Titles, parameters and labels come back in the site's language (Polish on
pl). An offer is one seller's listing (`offer_id`); a catalogue product
(`product_id`) groups many sellers' offers, and `product_offers()` lists every
seller's price for it. sk and hu calls can take up to about a minute; every
method raises the request timeout to at least 120s.

```python
from scavio import ScavioClient

client = ScavioClient()
al = client.allegro

# --- Search: price, price with delivery, sold count, seller, sponsored flag.
res = al.search("laptop", sort="price_low_to_high", condition="new")["data"]
print(res["total"], res["total_pages"], res["currency"], res["language"])
for item in res["items"][:5]:
    print(item["offer_id"], item["title"], item["price"], item["price_with_delivery"],
          item["sold_count"], item["seller"]["login"], item["placement"])

# --- One offer: 30-day lowest price on a discount, stock, delivery, seller.
o = al.offer(offer_id="18801787032")["data"]
print(o["price"], o["original_price"], o["lowest_price_30d"], o["discount_percent"])
print(o["stock"], o["sold_count"], o["seller"]["login"], o["seller"]["company_name"])
for d in o["delivery"][:3]:
    print(d["method"], d["price"], d["eta_text"])

# --- A catalogue product, then every seller's offer for it (price monitoring).
p = al.product(product_id="90d08230-e02a-4210-913d-d417453321b8")["data"]
print(p["title"], p["lowest_price"], p["offer_count"], p["rating"]["average"])
print(p["featured_offer"]["price"], p["featured_offer"]["seller"]["login"])
for r in p["reviews"][:3]:
    print(r["rating"], r["author"], r["text"])
offers = al.product_offers(product_id=p["product_id"],
                           sort="price_with_delivery_low_to_high")["data"]
for of in offers["offers"][:5]:
    print(of["seller"]["login"], of["price"], of["price_with_delivery"],
          of["smart"], of["is_featured"])

# --- A seller's offers, then the seller's feedback score.
s = al.seller("Yupilo_pl", query="lenovo", category="komputery")["data"]
print(s["seller"]["is_business"], [(c["name"], c["slug"]) for c in s["categories"]])
fb = al.seller_feedback("Yupilo_pl")["data"]
print(fb["summary"]["positive_percent"], fb["summary"]["super_seller"],
      fb["summary"]["member_since"])

# --- A category, and another market (Hungarian titles, HUF prices).
cat = al.category(category_id=491, sort="popularity")["data"]
print(cat["category"]["name"], cat["category"]["breadcrumb"], cat["total"])
hu = al.search("laptop", country="hu")["data"]
print(hu["currency"], hu["items"][0]["title"], hu["items"][0]["price"])
```

`search`, `category` and `seller` share one grid: 60 organic offers per page
(sponsored slots on top), up to 100 pages, exact `total` and every facet.
Sort by `relevance`, `price_low_to_high`, `price_high_to_low`,
`price_with_delivery_low_to_high`, `price_with_delivery_high_to_low`,
`popularity`, `ending_soonest` or `newest`; filter by `min_price` /
`max_price`, `condition` (`new` / `used`), `smart`, and on pl only
`buying_format` (`buy_now` / `auction`) and `deals` (Allegro's deals zone,
Black Weeks included while it runs); both pl-only filters are a 400
elsewhere. Each item carries `price`, `price_with_delivery`, `condition`,
`is_auction`, `discount_percent` and `lowest_price_30d`, the seller
(`super_seller`, `positive_feedback_percent`, `is_business`), `sold_count`,
`smart`, `placement` (regular, promoted, sponsored or featured) and `source`
(`allegro_lokalnie` for Allegro Lokalnie offers inside pl results).
`lowest_price_30d` is the EU disclosure Allegro shows next to a discount (the
lowest price in the 30 days before it): None without a discount, and not a
price history. `sold_count` is None on auctions and on cz, sk and hu offer
pages. `offer` returns the auction state (current price, minimum next bid,
ends at, has bids; no bid history), every parameter with GTIN and brand,
delivery methods, returns, warranty and `company_name` for business sellers.
`product` returns `lowest_price`, `offer_count`, the featured (buy box) offer,
the star distribution, review aspects and the first 20 reviews as shown on
the page. `seller` returns id, login, `is_business` and the seller's
categories (`slug` feeds `category`); super seller status, positive percent
and member since come from `seller_feedback` (20 ratings per page, no buyer
identity). Failed calls are not charged; a not-found is a charged 404. No
search suggestions, bidding, buying or checkout, Allegro Lokalnie as its own
source, Smart! account data, seller revenue, seller addresses or tax ids,
price history or reviews past the first 20: to track prices, poll and store
your own.

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
| Google | `search`, `custom_search`, `ai_mode`, `maps_search`, `maps_place`, `maps_reviews`, `shopping`, `shopping_product`, `shopping_stores`, `flights`, `hotels`, `hotels_detail`, `news`, `trends`, `trending` | 1 each |
| Amazon | `search`, `product`, `offers`, `options` | 1 each (`options` free) |
| Walmart | `search`, `product`, `stores`, `reviews`, `category`, `offers`, `seller`, `seller_products` | 1, except `search`/`category` on `domain="com.mx"` and store-targeted `search`/`product` (`delivery_zip` + `store_id`), which cost 2 |
| YouTube | `search`, `shorts`, `suggestions`, `video`, `metadata` (deprecated alias of `video`), `comments`, `comment_replies`, `transcript`, `related`, `channel_search`, `channel`, `channel_videos`, `channel_shorts`, `channel_community`, `channel_resolve`, `streams`, `community_post`, `community_post_comments` | `search`/`shorts` 2, `transcript` 5, `streams` 3, rest 1 each |
| Reddit | `search`, `search_suggestions`, `post`, `post_comments`, `comment_replies`, `subreddit`, `subreddit_posts`, `user`, `user_posts`, `user_comments`, `popular`, `trending`, `search_comments`, `search_subreddits` | 1 each |
| X | `search`, `tweet`, `tweet_comments`, `tweet_retweeters`, `user`, `user_tweets`, `user_replies`, `user_media`, `user_followers`, `user_followings`, `trending`, `search_communities`, `community`, `community_tweets` | 1 each |
| TikTok | `profile`, `user_posts`, `video`, `video_transcript`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings`, `trending_searches`, `trending_videos`, `search_suggestions`, `music`, `music_videos`, `search_music`, `music_chart`, `user_similar`, `user_playlists`, `playlist_videos`, `user_live`, `user_region` | 1 each |
| TikTok Shop | `search`, `search_suggestions`, `product`, `product_reviews`, `categories`, `category_products`, `shop_products`, `resolve` | 1 each |
| Instagram | `profile`, `user_posts`, `user_reels`, `user_tagged`, `user_stories`, `post`, `post_comments`, `comment_replies`, `search_users`, `search_hashtags`, `user_followers`, `user_followings`, `user_highlights`, `highlight_stories`, `search_reels`, `search_music`, `music_posts`, `search_locations`, `user_similar`, `post_likers` | Typically `profile`/`user_reels`/`user_tagged`/`music_posts` 1 (`user_reels`/`user_tagged` 2 the first time a username is looked up), every other method 2; `search_users`/`search_hashtags` with a `cursor` 8. Any call can cost up to 10 when it needs extra work; `credits_used` is the exact charge |
| LinkedIn | `person`, `person_about`, `person_posts`, `person_contact`, `company`, `company_posts`, `company_people`, `company_jobs`, `search_people`, `search_jobs`, `search_posts`, `job`, `post`, `post_comments` | `job` 30, `person_posts`/`company_posts`/`search_jobs`/`post_comments` 10 each, `person`/`person_about`/`company`/`post` 1 each; the five retired endpoints (`person_contact`, `company_people`, `company_jobs`, `search_people`, `search_posts`) return 410 and are never billed |
| Threads | `profile`, `user_posts`, `user_replies`, `post`, `post_comments`, `search_users` | 2, but `profile`/`user_posts`/`user_replies` cost 4 when addressed by `username` instead of `user_id` |
| Kuaishou | `profile`, `user_posts`, `user_live`, `user_resolve`, `video`, `video_comments`, `comment_replies`, `videos_batch`, `search`, `search_videos`, `search_users`, `search_live`, `tag_feed`, `trending` | priced per endpoint: `videos_batch` 40, `profile` and the four `search*` 10 each, `video` 2, the rest 1 |
| eBay | `search` (live or sold listings), `product`, `seller` | 1 each |
| Target | `search`, `category`, `product`, `reviews`, `availability` | 1 each |
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
| Lowe's | `stores` (start here), `search`, `product`, `reviews` | `reviews` 1, the rest 2 each |
| Sam's Club | `clubs`, `search`, `product`, `savings`, `category`, `reviews` | 1 each |
| Canadian Tire | `stores` (start here), `search`, `product`, `availability`, `clearance`, `deals` | 1 each |
| Dollar General | `stores` (start here), `search`, `product`, `deals`, `coupons` | 1 each |
| Sephora | `search`, `category`, `product` | 1 each, `product` 2 |
| Ulta Beauty | `search`, `category`, `product`, `stores` | 1 each |
| ALDI | `stores` (start here), `search`, `product` | 1 each |
| Micro Center | `stores` (start here), `search`, `product` | `stores` 1, the rest 2 each |
| Walgreens | `stores` (start here), `search`, `product`, `stock` | `stock` 4, the rest 2 each |
| CVS | `search`, `product`, `stock` | 1 each |
| Whole Foods Market | `stores` (start here), `store`, `search`, `category`, `deals`, `product`, `sales_flyer` | 1 each |
| Harbor Freight | `search`, `clearance`, `product`, `prices`, `stores`, `availability`, `reviews` | 1 each |
| PetSmart | `search`, `product`, `stores`, `store_stock`, `availability`, `deals` | 1 each |
| Petco | `search`, `category`, `product`, `stores`, `store_inventory` | 1 each |
| iHerb | `search`, `product`, `prices`, `reviews` | 2 each |
| Chewy | `search`, `product` | 10 each |
| Menards | `search`, `stores`, `product` | `search` 2; `stores` and `product` 1 each, `product` with `store_id` 2 |
| Nordstrom | `search`, `category`, `brand`, `product`, `reviews`, `availability`, `stores`, `suggestions` | `availability` and `reviews` 10, the rest 5 each |
| Nordstrom Rack (`nordstrom_rack`) | `search`, `category`, `brand`, `product`, `reviews`, `availability`, `stores`, `suggestions` | `availability` and `reviews` 10, the rest 5 each |
| Best Buy (`best_buy`) | `search`, `product`, `reviews`, `category`, `deals`, `stores`, `availability`, `suggestions`, `prices` | `stores` and `suggestions` 1; `deals` 3; `category` 2, 3 on a `pcmcat` page; the rest 2 each (`prices` per call, up to 15 SKUs; `availability` flat, up to 8 stores) |
| TCGplayer | `search`, `product`, `listings`, `price_history`, `sales`, `games`, `sets`, `price_guide`, `suggestions`, `trending`, `seller`, `seller_feedback`, `seller_products` | 1 each |
| Vinted | `search`, `product`, `seller`, `seller_products`, `seller_feedback`, `brands`, `suggestions`, `filters`, `categories` | 1 each |
| Macy's (`macys`) | `search`, `product`, `reviews`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions` | 1 each |
| Saks Fifth Avenue (`saks`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `designers` | 2 each |
| Kohl's (`kohls`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `coupons` | `stores` 1, the rest 2 each |
| JCPenney (`jcpenney`) | `search`, `product`, `category`, `brand`, `deals`, `stores`, `store_availability`, `suggestions`, `coupons`, `reviews`, `questions` | 1 each |
| Dick's Sporting Goods (`dicks`) | `search`, `product`, `products`, `reviews`, `category`, `brand`, `deals`, `store_availability`, `suggestions` | `product` and `reviews` 2, the rest 1 each |
| Foot Locker (`footlocker`) | `search`, `product`, `category`, `brand`, `deals`, `releases`, `stores`, `store_availability`, `reviews`, `questions` | 1 each |
| Fanatics (`fanatics`) | `search`, `product`, `browse`, `deals`, `reviews` | 1 each |
| Carrefour (`carrefour`) | `search`, `product`, `reviews`, `category`, `promotions`, `suggestions`, `stores`, `store_availability`, `store` | 1 each; `search` and `product` with `country="be"` 2 |
| Allegro (`allegro`) | `search`, `offer`, `product`, `product_offers`, `seller`, `seller_feedback`, `category` | 2 each |
| Trustpilot | `search`, `business`, `reviews`, `categories`, `category`, `review` | 2 each |
| Mercado Libre | `search`, `product`, `reviews`, `questions`, `best_sellers` | `reviews` 1, the rest 2 each |
| ChatGPT | `prompt` | 5 per answered prompt |
| Gemini | `prompt` | 5 per answered prompt |
| Extract (core, callable) | `client.extract(url)`, `extract.map`, `extract.crawl`, `extract.crawl_status`, `extract.cancel_crawl`, `extract.batch`, `extract.batch_status`, `extract.cancel_batch` | `extract`: 1 for `mode="normal"` or `"advanced"`, 2 for `"ultra"`, only on success. `map`: 1 on normal. `crawl` / `batch`: that same price per successful page. Status and cancel: free |

Every method's full parameter list is available inline in your editor (typed
keyword arguments with docstrings). See the [API docs](https://scavio.dev/docs?utm_source=pypi-scavio&utm_medium=package&utm_campaign=readme)
for field-level details.

### Changed in 0.51.0

- **New `allegro` namespace** (sync and async) for Allegro, 7 endpoints at
  2 credits each: `search`, `offer`, `product`, `product_offers`, `seller`,
  `seller_feedback`, `category`. Every endpoint takes `country` pl
  (default), cz, sk or hu; `buying_format` and `deals` are pl only. 120s
  timeout floor.

### Changed in 0.50.0

- **New `carrefour` namespace** (sync and async) for Carrefour, 9 endpoints
  at 1 credit each: `search`, `product`, `reviews`, `category`,
  `promotions`, `suggestions`, `stores`, `store_availability`, `store`.
  carrefour.fr serves every endpoint; `search` and `product` also take
  `country` ar, ro or be (`language` fr or nl; 2 credits on be). `store`
  scopes prices and assortment to one store. 120s timeout floor.

### Changed in 0.49.1

- `fanatics` docstrings: price sorts order by the current `price`, not the
  with-code price; department and filter ids are per store; the players
  facet appears only on some pages; `price_label` `coupon` means
  coupon-eligible; product `on_sale` covers clearance markdowns.

### Changed in 0.49.0

- **New `fanatics` namespace** (sync and async) for Fanatics merchandise,
  5 endpoints at 1 credit each: `search`, `product`, `browse`, `deals`,
  `reviews`. `country` picks one of 8 storefronts (us default, gb, de, fr,
  es, it, jp, ca), `language` the ca language and `site` a US league store
  (nflshop, mlbshop, nhlshop, mlsstore); `reviews` is US only. 120s timeout
  floor, 300s for `reviews`.

### Changed in 0.48.0

- **New `footlocker` namespace** (sync and async) for Foot Locker, 10
  endpoints at 1 credit each: `search`, `product`, `category`, `brand`,
  `deals`, `releases`, `stores`, `store_availability`, `reviews`,
  `questions`. `country` picks one of 13 storefronts (us default, ca, gb,
  de, fr, it, es, nl, be, at, ie, au, nz) and `language` the ca / be
  language; `releases` covers us, ca and gb and takes `date_from` /
  `date_to`; `stores`, `store_availability`, `reviews` and `questions` are
  US only. 120s timeout floor, 240s for `reviews` and `questions`.

### Changed in 0.47.0

- **New `dicks` namespace** (sync and async) for dickssportinggoods.com
  (Dick's Sporting Goods, US, USD), 9 endpoints: `search`, `product`,
  `products`, `reviews`, `category`, `brand`, `deals`,
  `store_availability`, `suggestions`, 1 credit each except `product` and
  `reviews` (2). The grid endpoints take `brand`, `page_size` (up to 144),
  a `sort`, `min_price` / `max_price` and any facet via `filters` (a dict);
  `product` returns per-SKU prices and online units; `products` takes up to
  5 `product_ids`; `store_availability` takes a list of `skus` and an
  optional `chain` (Golf Galaxy, Public Lands). 120s timeout floor, 240s
  for `product` and `reviews`.

### Changed in 0.46.0

- **`jcpenney.reviews` and `jcpenney.questions`** (sync and async), 1 credit
  each, taking `product_id` or `url`. `reviews` returns review text (up to
  98, `sort`, one-star `rating` filter, `max_reviews`) with `total_reviews`,
  `displayed_reviews` and `matching_reviews`; `questions` returns questions
  and every answer with `author_type` and `ai_label` (up to 50,
  `max_questions`). Both raise the request timeout to at least 240s: they
  usually take 15-90s, up to about 3 minutes.

### Changed in 0.45.0

- **New `jcpenney` namespace** (sync and async) for jcpenney.com (US incl.
  Puerto Rico stores, USD), 9 endpoints at 1 credit each: `search`,
  `product`, `category`, `brand`, `deals`, `stores`, `store_availability`,
  `suggestions`, `coupons`. The grid endpoints take `brand`, `color`,
  `size`, `price_range`, `deal` (one value or a list), a `sort` and any
  facet via `filters` (a dict); `product` takes up to 20 `product_ids`;
  `store_availability` takes a required `sku` and returns unit counts at the
  5 nearest stores. 120s timeout floor on every method.

### Changed in 0.44.0

- **New `kohls` namespace** (sync and async) for kohls.com (US, USD), 9
  endpoints: `search`, `product`, `category`, `brand`, `deals`, `stores`,
  `store_availability`, `suggestions`, `coupons`. 2 credits each, `stores`
  1. The grid endpoints take `brand`, `color`, `size`, `on_sale`,
  `clearance`, a `sort` (incl. `percent_off`, `highest_rated`) and facet
  value ids via `filters` (one or a list); `store_availability` takes a
  required `sku` and `zip`. 120s timeout floor on every method.

### Changed in 0.43.0

- **New `saks` namespace** (sync and async) for saksfifthavenue.com (US,
  USD), 9 endpoints at 2 credits each: `search`, `product`, `category`,
  `brand`, `deals`, `stores`, `store_availability`, `suggestions`,
  `designers`. The grid endpoints take `brand`, `color`, `size`, a price
  range, `on_sale`, `new_arrivals`, any facet via `filters` (a dict) and
  `start` / `page` paging; `store_availability` takes a required variant
  `sku`. 120s timeout floor on every method.

### Changed in 0.42.0

- **New `macys` namespace** (sync and async) for macys.com (US, USD), 9
  endpoints at 1 credit each: `search`, `product`, `reviews`, `category`,
  `brand`, `deals`, `stores`, `store_availability`, `suggestions`. The grid
  endpoints take `brand`, `color`, `special_offer`, a price range,
  `pickup_store_id`, any facet via `filters` (a dict) and
  `include_sponsored`; `product` takes up to 10 `product_ids` in one call.
  120s timeout floor on every method.

### Changed in 0.41.1

- **`vinted`:** the `country` docs now say what Vinted actually does: every
  site, `uk`, `us` and `au` included, can show listings from sellers in other
  countries, priced in the site's currency, and `product` returns the seller's
  own price and currency. `filters(category_id=...)` now narrows the options
  to that category (a server-side fix; no SDK signature change).

### Changed in 0.41.0

- **New `vinted` namespace** (sync and async) for Vinted on 27 country sites
  (`country`, `fr` default), 9 endpoints at 1 credit each: `search`,
  `product`, `seller`, `seller_products`, `seller_feedback`, `brands`,
  `suggestions`, `filters`, `categories`. `search` and `seller_products`
  return the price, the Vinted fee (`service_fee`) and `total_price`; the id
  filters (`brand_ids`, `status_ids`, `size_ids`, `color_ids`,
  `material_ids`) take a list or a comma-separated string. 120s timeout floor
  on every method.

### Changed in 0.40.0

- **New `tcgplayer` namespace** (sync and async) for tcgplayer.com (US, USD),
  13 endpoints at 1 credit each: `search`, `product`, `listings`,
  `price_history`, `sales`, `games`, `sets`, `price_guide`, `suggestions`,
  `trending`, `seller`, `seller_feedback`, `seller_products`. `product`
  returns the market price per SKU (condition x printing x language) with the
  recent sale range; `price_history` returns up to a year of sold volume per
  SKU. 120s timeout floor on every method.

### Changed in 0.39.0

- **New `best_buy` namespace** (sync and async) for bestbuy.com (US):
  `search`, `product`, `reviews`, `category`, `deals`, `stores`,
  `availability`, `suggestions`, `prices`. `product` returns open-box offers
  by condition (fair, good, excellent) with savings against new and regular;
  `availability` returns per-store pickup status at up to 8 stores; `prices`
  takes up to 15 SKUs per call. 120s timeout floor on every method.

### Changed in 0.38.0

- **New `nordstrom_rack` namespace** (sync and async) for nordstromrack.com
  (US): `search`, `category`, `brand`, `product`, `reviews`, `availability`,
  `stores`, `suggestions`, with the same parameters, credits (5 each,
  `availability` and `reviews` 10) and timeout floors (120s, `reviews` 150s)
  as `nordstrom`. `category` takes `/shop` and `/clearance` paths, including
  Clear the Rack and flash events (`/shop/flash/event-N`); `brand` takes
  `/brands/<slug>`. Product and listing rows carry `clearance_price_range`,
  `promotion_price_range` and `promotion_percent_off`.

### Changed in 0.37.0

- `nordstrom.reviews(*, url, style_id, sort, stars, verified_only, with_photos,
  search, max_reviews)` (sync and async), 10 credits: a product's full review
  history, up to 200 per call (default 60), sorted `most_helpful` (default),
  `most_recent`, `highest_rated` or `lowest_rated`, filtered by star ratings,
  verified purchases, photos or a text search (`search` cannot be combined
  with `sort`). Returns the review summary (average, histogram, size and width
  rating, praised and criticized features with a quote, rating-only count),
  the AI review summary, `total_results`, `returned` and `has_more`. Calls take
  20-60s (up to about 100s at 200 reviews), so this method's timeout floor is
  150s.

### Changed in 0.36.0

- `nordstrom` gains five methods (sync and async), all with the 120s timeout floor:
  - `category(category, *, page, sort)`, 5 credits: a /browse category path or
    URL (departments, `sale/women`, `/browse/new`), 24 products a page plus the
    category's breadcrumbs, subcategories and the filter sidebar with counts.
  - `brand(brand, *, page, sort)`, 5 credits: a /brands path or URL (a product's
    `brand_url` works), same rows and filters.
  - `stores(*, zip, latitude, longitude, store_numbers, distance_miles)`, 5
    credits: pass exactly one of `zip`, `latitude` + `longitude`, or
    `store_numbers` (list or comma-separated string); radius 1-100 miles,
    default 100.
  - `availability(*, url, style_id, sku_id)`, 10 credits: per sku ship
    quantity, pickup quantity (chain-wide) and the stores that can do pickup.
  - `suggestions(query, *, limit)`, 5 credits: search-box autocomplete, 1-20,
    default 8.

### Changed in 0.35.0

- **New `nordstrom` namespace** (sync and async), 5 credits per call.
  - `search(query, *, page, sort)`: nordstrom.com (US), 24 products a page.
    `sort`: relevance, rating, price_high, price_low, newest, percent_off.
  - `product(*, url, style_id)`: pass one. Every color and size as a sku with
    sku id, UPC, price, original price, percent off, price type, in_stock and
    quantity available to ship; star histogram, size-fit distribution and the
    reviews shown on the product page.
  - Both raise the request timeout to 120s.

### Changed in 0.34.0

- `menards.search(query, store_id, ...)` (sync and async), 2 credits: menards.com
  search at one store, 40 products a page, with price, sale price, the mail-in
  rebate, final price and that store's stock count. `sort` (relevance,
  price_asc, price_desc, brand_asc, brand_desc; price sorts use the everyday
  price), `in_stock_today`, `min_price`, `max_price`, `page`. An unknown store
  number is a 400.

### Changed in 0.33.0

- **Seven new US retail namespaces, 33 methods** (sync and async).
  - `whole_foods`: `search`, `category`, `deals`, `product`, `stores`, `store`,
    `sales_flyer` (1 credit each). Prices are one store's (5-digit `store_id`,
    default 10145): regular, sale and Prime member price. `product` returns the
    in-store and online price as separate blocks. Search sorts by relevance or
    price only.
  - `harbor_freight`: `search`, `clearance`, `product`, `prices` (up to 50
    item numbers), `stores`, `availability`, `reviews` (1 each). National
    prices with sale end date, coupon, Inside Track Club member price and
    compare-at. Store stock is a status plus aisle from a daily snapshot.
  - `petsmart`: `search`, `product`, `stores`, `store_stock`, `availability`,
    `deals` (1 each). Autoship first-order and recurring prices; stock is a unit
    count per store. `availability` takes `pairs` of `{"store_id", "sku"}`.
  - `petco`: `search`, `category`, `product`, `stores`, `store_inventory` (1
    each). `store_inventory` takes `cat_entry_ids`, not part numbers.
    `category` and `product` can take 10-30 seconds, so their request timeout
    is raised to 120s.
  - `iherb`: `search`, `product`, `prices` (up to 50 ids), `reviews` (2 each).
    Online only, US/USD; `reviews` is the rating summary and histogram with the
    top positive and top critical review.
  - `chewy`: `search`, `product` (10 each). One-time, Autoship and
    first-Autoship prices and MAP fields; `search` reports a category redirect.
  - `menards`: `product`, `stores` (1 each; `product` with `store_id` 2, adds
    stock quantity and aisle). No search. `product` timeout raised to 120s.

### Changed in 0.32.1

- `cvs.search`: `same_day_delivery` is now always `None`, as on `cvs.stock`. CVS
  reports one same-day count per SKU whichever store is sent, so it was not the
  store's number.

### Changed in 0.32.0

- **Six new US retail namespaces, 20 methods** (sync and async).
  - `sephora`: `search`, `category`, `product` (1 credit each). `product` takes
    `url` or `product_id` and returns a review summary with pro/con sentiment
    counts (no review text).
  - `ulta`: `search`, `category`, `product`, `stores` (1 each). `stores` is in
    stock / out of stock for one shade at the 10 stores nearest a ZIP.
  - `aldi`: `search`, `product`, `stores` (1 each). Pass `store_id` or `zip`;
    `service_type` picks the in-store (default), pickup or delivery price.
  - `micro_center`: `search`, `product` (2 each), `stores` (1). Stock is per
    3-digit `store_id` (web store 029 when omitted), capped at 25+.
  - `walgreens`: `search`, `product`, `stores` (2 each), `stock` (4, up to 20
    stores). Prices are national.
  - `cvs`: `search`, `product`, `stock` (1 each, `stock` up to 20 SKUs). No
    store locator; `search` defaults to store 7019. `product` can take 10-30+
    seconds, so its request timeout is raised to 120s.

### Changed in 0.31.0

- **Four new store-level retail namespaces, 21 methods** (sync and async). Every
  method answers for one store or club you choose.
  - `lowes`: `search`, `product`, `stores` (2 credits each), `reviews` (1).
    `store_id` and the store's `zip` are required on `search` and `product`;
    `search(on_sale=True)` returns that store's deals.
  - `sams_club`: `search`, `product`, `clubs`, `savings`, `category`, `reviews`
    (1 each). `product(club_id=...)` prices and stocks one club; clearance is
    `category("1150109")`.
  - `canadian_tire`: `search`, `product`, `stores`, `availability` (up to 50
    SKUs), `clearance`, `deals` (1 each). `store_id` is required except on
    `stores`.
  - `dollar_general`: `search`, `product`, `stores` (pass `upc` for per-store
    unit counts at up to 25 stores), `deals` (`on_sale` or `clearance`),
    `coupons` (1 each).

### Changed in 0.27.0

- **New `target.availability(tcin, zip, radius=None, store_id=None)`.** In-store
  stock for one product at every Target store near a 5-digit US ZIP: units,
  in-store, pickup, curbside and ship-to-store status, distance, address and
  hours, up to 20 stores. `store_id` narrows the result to one store. 1 credit.

  ```python
  stock = client.target.availability("85978609", "79407")
  for s in stock["data"]["stores"]:
      print(s["store_id"], s["name"], s["quantity"], s["in_store"], s["pickup"])
  ```
- `store_id` on `target.search`, `category`, `product` and `reviews` sets the
  store for prices only; its docstring no longer mentions availability. No
  behaviour change.

### Changed in 0.26.2

- `chatgpt.prompt` now costs 2 credits per answered prompt. Gemini stays at 5.

### Changed in 0.26.1

- `chatgpt.prompt` now costs 1 credit per answered prompt (was 5). Gemini stays at 5.

### Changed in 0.26.0

- New `chatgpt.prompt` and `gemini.prompt` (sync and async): send a prompt, get the assistant's
  answer with cited sources, web searches (ChatGPT) and recommended products
  (`POST /api/v1/chatgpt/prompt`, `POST /api/v1/gemini/prompt`). 5 credits per answered prompt at launch.
- Endpoints can now declare a minimum request timeout; these two raise it to 120s when the
  client's `timeout` is shorter. A longer client timeout is always kept.

### Changed in 0.25.0

- New `google.custom_search` (sync and async): Google search in the Custom Search JSON API
  format (`POST /api/v1/google/customsearch`). Snake_case arguments map to the CSE wire names
  (`site_search` -> `siteSearch`, `date_restrict` -> `dateRestrict`, ...). 1 credit.

### Changed in 0.24.1

- Docstring wording only: parameter notes describe what each endpoint returns. No price, parameter or behavior changed.

### Changed in 0.24.0

- **Instagram is cheaper.** Typical costs are now 1-2 credits instead of 8-10:
  `profile`, `user_reels`, `user_tagged` and `music_posts` 1 (`user_reels` /
  `user_tagged` 2 the first time a username is looked up), everything else 2.
  `search_users` / `search_hashtags` with a `cursor` cost 8. Any call can cost
  up to 10 when it needs extra work; `credits_used` is always the exact charge.
- **8 new Instagram methods**, sync and async:
  `user_highlights(*, username=None, user_id=None)`,
  `highlight_stories(highlight_id)`,
  `user_similar(*, username=None, user_id=None)`,
  `post_likers(*, shortcode=None, url=None)`,
  `search_reels(keyword, *, cursor=None)`, `search_music(keyword)`,
  `music_posts(music_id, *, cursor=None)` and `search_locations(keyword)`.
- `user_posts` still returns its existing shape: items under `data.data.items`,
  next page via `data.pagination_token`.

```python
hl = client.instagram.user_highlights(username="natgeo")
stories = client.instagram.highlight_stories("highlight:18149897764550869")
track_reels = client.instagram.music_posts("1747512212697470")
```

### Changed in 0.23.0

- **`client.extract` is now a callable namespace.** `client.extract(url,
  format=..., mode=...)` works exactly as before (same signature, same request
  on the wire, sync and async), and the same object adds the website map,
  crawl and batch operations: `extract.map`, `extract.crawl`,
  `extract.crawl_status`, `extract.cancel_crawl`, `extract.batch`,
  `extract.batch_status`, `extract.cancel_batch`. `crawl` and `batch` take
  `wait=True` to poll until done and return every result. See example 17b.
- **`scavio.verify_webhook(secret, header, body)`** verifies the signed
  completion webhooks crawl and batch jobs send.
- New `ScavioJobTimeoutError` (a `ScavioTimeoutError`) when `wait_timeout`
  elapses; it carries `job_id`.
- **`tiktok.video_transcript(video_id=None, *, url=None, language=None)`**:
  the spoken-word transcript of a TikTok video as timestamped segments and full
  text, 1 credit. Returns `available: false` for videos with no spoken captions.
- 2xx responses other than 200 (a job's 202) are now treated as success.

```python
site = client.extract.map("https://scavio.dev", limit=50)
crawl = client.extract.crawl("https://scavio.dev/docs", max_pages=2, wait=True)
words = client.tiktok.video_transcript("7609177768793787679")
```

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
