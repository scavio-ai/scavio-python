# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev) Search API. Access real-time data from Google, Amazon, Walmart, YouTube, Reddit, X, TikTok, TikTok Shop, Instagram, and LinkedIn with a single API key. Built for AI agents, LLM applications, and data pipelines.

> One API key, ten data sources, structured JSON with knowledge graphs. A powerful alternative to Tavily, SerpAPI, and ScraperAPI for developers who need more than just web search.

## Why Scavio

| Feature | Scavio | Tavily | SerpAPI | ScraperAPI |
|---------|--------|--------|---------|------------|
| Google Search | Yes | Yes | Yes | Yes |
| Amazon Products | Yes | No | Yes | No |
| Walmart Products | Yes | No | No | No |
| YouTube Search | Yes | No | Yes | No |
| Reddit Data (12 endpoints) | Yes | No | No | No |
| X Data (11 endpoints) | Yes | No | No | No |
| TikTok Data (11 endpoints) | Yes | No | No | No |
| TikTok Shop Data (8 endpoints) | Yes | No | No | No |
| Instagram Data (12 endpoints) | Yes | No | No | No |
| LinkedIn Data (9 endpoints) | Yes | No | No | No |
| Data Sources | 10 | 1 | 1 per plan | 1 |
| Structured JSON | Yes | Yes | Yes | Raw HTML |
| Knowledge Graphs | Yes | No | Yes | No |
| Async Client | Yes | Yes | No | No |
| Single API Key | Yes | Yes | No | No |
| Rate Limiting Built-in | Yes | No | No | No |
| Automatic Retries + Backoff | Yes | No | No | No |
| Fully Typed Parameters | Yes | No | No | No |
| Type Hints (PEP 561) | Yes | Yes | No | No |

Tavily focuses on AI-optimized web search. SerpAPI offers SERP parsing across search engines with separate plans. ScraperAPI provides raw web scraping with proxy rotation. Scavio combines multi-source structured data in a single [search API for AI agents](https://scavio.dev/search-api-for-ai-agents) with one SDK and one API key.

## Installation

```bash
pip install scavio
```

## Quick Start

Get your free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev).

```python
from scavio import ScavioClient

client = ScavioClient(api_key="sk_...")  # or set SCAVIO_API_KEY env var

results = client.search("best noise cancelling headphones 2026")
for r in results["organic_results"]:
    print(r["title"], r["link"])
```

Every method returns the API response as a plain `dict`. Amazon responses are
normalized to a stable, documented shape; the other endpoints pass the upstream
provider's shape through, so fields vary by endpoint.

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

> **Retired endpoints.** The upstream provider withdrew the datasets behind
> `person_contact`, `company_people`, `company_jobs`, `search_people` and
> `search_posts`. They remain callable but always return HTTP 410 and are never
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
# (upstream masks it), and it resolves only about 44% of the ids search returns.
# A 404 there is a normal outcome, not an error: skip the item, do not retry.
from scavio import NotFoundError

product_id = results["data"]["products"][0]["product_id"]
try:
    detail = client.tiktok_shop.product(product_id)
    print(detail["data"]["title"], len(detail["data"]["variants"]), "variants")
except NotFoundError:
    pass  # no detail data upstream for this product; skip it, do not retry

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
    max_requests_per_second=1,           # client-side rate limit (1-10)
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
| Walmart | `search`, `product` | 1 each |
| YouTube | `search`, `shorts`, `suggestions`, `video`, `metadata` (deprecated alias of `video`), `comments`, `comment_replies`, `transcript`, `related`, `channel_search`, `channel`, `channel_videos`, `channel_shorts`, `channel_community`, `channel_resolve`, `streams` | `search`/`shorts` 2, `transcript` 8, `streams` 3, rest 1 each |
| Reddit | `search`, `search_suggestions`, `post`, `post_comments`, `comment_replies`, `subreddit`, `subreddit_posts`, `user`, `user_posts`, `user_comments`, `popular`, `trending` | 1 each |
| X | `search`, `tweet`, `tweet_comments`, `tweet_retweeters`, `user`, `user_tweets`, `user_replies`, `user_media`, `user_followers`, `user_followings`, `trending` | 1 each |
| TikTok | `profile`, `user_posts`, `video`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings` | 1 each |
| TikTok Shop | `search`, `search_suggestions`, `product`, `product_reviews`, `categories`, `category_products`, `shop_products`, `resolve` | 1 each |
| Instagram | `profile`, `user_posts`, `user_reels`, `user_tagged`, `user_stories`, `post`, `post_comments`, `comment_replies`, `search_users`, `search_hashtags`, `user_followers`, `user_followings` | `user_posts` 2, `post`/`comment_replies` 8, the other nine 10 each |
| LinkedIn | `person`, `person_about`, `person_posts`, `person_contact`, `company`, `company_posts`, `company_people`, `company_jobs`, `search_people`, `search_jobs`, `search_posts`, `job`, `post`, `post_comments` | `job` 30, `person_posts`/`company_posts`/`search_jobs`/`post_comments` 10 each, `person`/`person_about`/`company`/`post` 1 each; the five retired endpoints (`person_contact`, `company_people`, `company_jobs`, `search_people`, `search_posts`) return 410 and are never billed |

Every method's full parameter list is available inline in your editor (typed
keyword arguments with docstrings). See the [API docs](https://scavio.dev/docs)
for field-level details.

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

Amazon moved to a new upstream and the API now returns a normalized shape
instead of the previous raw provider payload.

- `search` returns `{query, page, total_results, total_results_text, count, products[], filters[], related_searches[]}`.
  Each product is `{asin, title, url, image, price, currency, rating, reviews_count, is_sponsored, position, badge, sales_volume, delivery{is_free, date, fastest_date}}`.
- `product` returns flat fields: `price`, `list_price`, `currency`, `rating`, `reviews_count`, `features`, `images`, `videos`, `variants`, `specifications`, `best_sellers_rank`, `shipping`, and more. The old `buybox[]` array no longer exists -- use `offers` for per-seller pricing.
- `offers` is new: every seller for one ASIN, with `price`, `condition`, `seller_name`, `is_buy_box_winner`, `is_fulfilled_by_amazon`, and delivery windows.
- `country` (ISO 3166-1 alpha-2: `us`, `gb`, `de`) is the marketplace selector and replaces `domain`. `page` replaces `start_page`. The old names still work as deprecated aliases.
- Nine parameters were removed: `language`, `currency`, `device`, `sort_by`, `pages`, `category_id`, `merchant_id`, `zip_code`, `autoselect_variant`. `sort_by` in particular was verified to be ignored by the marketplace, so result sorting is not available at any layer. Sending one of them anyway (via `**extra`) still returns 200, with a top-level `warnings` array explaining what was ignored.
- `options` still returns `domains` and `countries`; `languages` and `currencies` are now always empty, because neither is a request parameter any more.

## Links

- [Website](https://scavio.dev)
- [Documentation](https://docs.scavio.dev)
- [Dashboard & API Keys](https://dashboard.scavio.dev)
- [API Reference](https://docs.scavio.dev/api-reference)
- [Compare Scavio vs alternatives](https://scavio.dev/compare)

## License

MIT


## About Scavio

[Scavio](https://scavio.dev) is a unified [search API](https://scavio.dev/docs/search-api) built for AI agents — one API key, structured JSON, no scraping or proxies. A real-time [Tavily alternative](https://scavio.dev/alternatives/tavily) and [SerpAPI alternative](https://scavio.dev/alternatives/serpapi) with data from:

- [Google Search API](https://scavio.dev/google-search-api) — SERP results, news, images, maps, and knowledge graph
- [Amazon Product API](https://scavio.dev/amazon-product-api) and [Walmart Product API](https://scavio.dev/walmart-product-api) — product search and details
- [YouTube API](https://scavio.dev/youtube-transcript-api), [TikTok API](https://scavio.dev/tiktok-api), and [Instagram API](https://scavio.dev/instagram-api) — video and social media data
- [TikTok Shop API](https://scavio.dev/docs/tiktok-shop-search) — product search, detail, reviews, categories, and shop catalogs
- [Reddit API](https://scavio.dev/reddit-api) — posts, comments, subreddits, and trending
- [X API](https://scavio.dev/docs/x-search) and [LinkedIn API](https://scavio.dev/docs/linkedin-person) — tweets, profiles, companies, and jobs

For a detailed head-to-head breakdown, see [Tavily vs Scavio](https://scavio.dev/compare/tavily/vs-scavio).

Get a free [API key](https://dashboard.scavio.dev) and explore the [documentation](https://scavio.dev/docs/introduction).
