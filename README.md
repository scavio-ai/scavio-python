# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev) Search API. Access real-time data from Google, Amazon, Walmart, YouTube, Reddit, TikTok, and Instagram with a single API key. Built for AI agents, LLM applications, and data pipelines.

> One API key, six data sources, structured JSON with knowledge graphs. A powerful alternative to Tavily, SerpAPI, and ScraperAPI for developers who need more than just web search.

## Why Scavio

| Feature | Scavio | Tavily | SerpAPI | ScraperAPI |
|---------|--------|--------|---------|------------|
| Google Search | Yes | Yes | Yes | Yes |
| Amazon Products | Yes | No | Yes | No |
| Walmart Products | Yes | No | No | No |
| YouTube Search | Yes | No | Yes | No |
| Reddit Search | Yes | No | No | No |
| TikTok Data (11 endpoints) | Yes | No | No | No |
| Instagram Data (12 endpoints) | Yes | No | No | No |
| Data Sources | 6 | 1 | 1 per plan | 1 |
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

Every method returns the raw API response as a plain `dict` (response shapes are
passed through from the upstream providers and vary by endpoint).

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
client.amazon.product("B09XS7JWHH", domain="co.uk", currency="GBP")
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
amazon = client.amazon.search(query, domain="com")
walmart = client.walmart.search(query)

print("Amazon:")
for p in amazon["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")

print("\nWalmart:")
for p in walmart["data"]["products"][:3]:
    print(f"  ${p['price']} - {p['title'][:60]}")
```

### 3. Product Lookup by ASIN

```python
from scavio import ScavioClient

client = ScavioClient()

product = client.amazon.product("B0BS1PRC4L")
data = product["data"]

print(f"Brand:   {data['brand']}")
print(f"Title:   {data['title']}")
print(f"Rating:  {data['rating']} ({data['reviews_count']} reviews)")
print(f"Price:   ${data['buybox'][0]['price']}")
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
    title = v["title"]["runs"][0]["text"]
    views = v.get("viewCountText", {}).get("simpleText", "N/A")
    print(f"{title} ({views})")
    print(f"  https://youtube.com/watch?v={v['videoId']}")

# Get detailed metadata for a specific video
meta = client.youtube.metadata("dQw4w9WgXcQ")
print(f"\n{meta['data']['title']}")
print(f"  {meta['data']['view_count']:,} views, {meta['data']['like_count']:,} likes")
```

### 7. Reddit Market Research

```python
from scavio import ScavioClient

client = ScavioClient()

posts = client.reddit.search("best mechanical keyboard", sort="hot")

for post in posts["data"]["posts"]:
    print(f"r/{post['subreddit']} - {post['title']}")
    print(f"  {post['url']}")
    print()
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

### 10. Social Media Monitoring

```python
from scavio import ScavioClient

client = ScavioClient()

brand = "scavio"
reddit = client.reddit.search(brand, sort="hot")
tiktok = client.tiktok.search_videos(brand, count=5)

print(f"Reddit mentions ({len(reddit['data']['posts'])}):")
for post in reddit["data"]["posts"][:3]:
    print(f"  r/{post['subreddit']}: {post['title']}")

tiktok_videos = tiktok["data"].get("search_item_list", [])
print(f"\nTikTok mentions ({len(tiktok_videos)}):")
for v in tiktok_videos[:3]:
    desc = v["aweme_info"].get("desc", "No description")
    print(f"  {desc[:80]}")
```

### 11. Price Drop Alert

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

### 12. Async Multi-Source Search

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient() as client:
        google = await client.search("mechanical keyboard")
        amazon = await client.amazon.search("mechanical keyboard", domain="com")

        print(f"Google: {len(google['organic_results'])} results")
        print(f"Amazon: {len(amazon['data']['products'])} products")

        for r in google["organic_results"][:3]:
            print(f"  Web: {r['title'][:60]}")
        for p in amazon["data"]["products"][:3]:
            print(f"  Amazon: ${p['price']} - {p['title'][:50]}")

asyncio.run(main())
```

### 13. Check API Usage

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
| Amazon | `search`, `product`, `options` | 1 each (`options` free) |
| Walmart | `search`, `product` | 1 each |
| YouTube | `search`, `metadata` | 1 each |
| Reddit | `search`, `post` | 2 each |
| TikTok | `profile`, `user_posts`, `video`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings` | 1 each |
| Instagram | `profile`, `user_posts`, `user_reels`, `user_tagged`, `user_stories`, `post`, `post_comments`, `comment_replies`, `search_users`, `search_hashtags`, `user_followers`, `user_followings` | 2 each |

Every method's full parameter list is available inline in your editor (typed
keyword arguments with docstrings). See the [API docs](https://scavio.dev/docs)
for field-level details.

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
- [Reddit API](https://scavio.dev/reddit-api) — posts and threaded comments

For a detailed head-to-head breakdown, see [Tavily vs Scavio](https://scavio.dev/compare/tavily/vs-scavio).

Get a free [API key](https://dashboard.scavio.dev) and explore the [documentation](https://scavio.dev/docs/introduction).
