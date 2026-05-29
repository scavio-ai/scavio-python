# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio.svg)](https://pypi.org/project/scavio/)
[![Downloads](https://img.shields.io/pypi/dm/scavio.svg)](https://pypi.org/project/scavio/)
[![Python](https://img.shields.io/pypi/pyversions/scavio.svg)](https://pypi.org/project/scavio/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev) Search API. Access real-time data from Google, Amazon, Walmart, YouTube, Reddit, and TikTok with a single API key. Built for AI agents, LLM applications, and data pipelines.

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
| Data Sources | 6 | 1 | 1 per plan | 1 |
| Structured JSON | Yes | Yes | Yes | Raw HTML |
| Knowledge Graphs | Yes | No | Yes | No |
| Async Client | Yes | Yes | No | No |
| Single API Key | Yes | Yes | No | No |
| Rate Limiting Built-in | Yes | No | No | No |
| Type Hints (PEP 561) | Yes | Yes | No | No |

Tavily focuses on AI-optimized web search. SerpAPI offers SERP parsing across search engines with separate plans. ScraperAPI provides raw web scraping with proxy rotation. Scavio combines multi-source structured data in a single SDK with one API key.

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
for r in results["results"]:
    print(r["title"], r["url"])
```

## Examples

### 1. AI Web Research -- Feed Search Results to an LLM

```python
from scavio import ScavioClient

client = ScavioClient()

results = client.search("latest advances in quantum computing 2026")

context = "\n\n".join(
    f"[{r['title']}]({r['url']})\n{r['content']}"
    for r in results["results"]
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

results = client.search("best project management software", country_code="us")

domains = {}
for r in results["results"]:
    domain = r["domain"]
    domains[domain] = domains.get(domain, 0) + 1

print("Domains ranking for this keyword:")
for domain, count in sorted(domains.items(), key=lambda x: -x[1]):
    print(f"  {domain}: {count} result(s)")
```

### 5. News Aggregation

```python
from scavio import ScavioClient

client = ScavioClient()

news = client.google.search("AI startups", search_type="news")

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

### 9. Social Media Monitoring

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

### 10. Price Drop Alert

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

### 11. Async Multi-Source Search

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient() as client:
        google = await client.search("mechanical keyboard")
        amazon = await client.amazon.search("mechanical keyboard", domain="com")

        print(f"Google: {len(google['results'])} results")
        print(f"Amazon: {len(amazon['data']['products'])} products")

        for r in google["results"][:3]:
            print(f"  Web: {r['title'][:60]}")
        for p in amazon["data"]["products"][:3]:
            print(f"  Amazon: ${p['price']} - {p['title'][:50]}")

asyncio.run(main())
```

### 12. Check API Usage

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
```

## Configuration

```python
client = ScavioClient(
    api_key="sk_...",
    base_url="https://api.scavio.dev",  # custom base URL
    timeout=30,                          # request timeout in seconds
    max_requests_per_second=1,           # rate limiting (1-10)
)
```

## Integrations

Scavio works with popular AI/LLM frameworks:

- [LangChain](https://github.com/scavio-ai/langchain-scavio) -- `pip install langchain-scavio`
- [MCP Server](https://www.npmjs.com/package/@scavio/mcp-server) -- for Claude, Cursor, and other MCP clients
- [n8n](https://www.npmjs.com/package/n8n-nodes-scavio) -- no-code workflow automation

## API Reference

| Service | Endpoints | Credits |
|---------|-----------|---------|
| Google | `search` | 1-2 |
| Amazon | `search`, `product` | 1 each |
| Walmart | `search`, `product` | 1 each |
| YouTube | `search`, `metadata` | 1 each |
| Reddit | `search`, `post` | 2 each |
| TikTok | `profile`, `user_posts`, `video`, `video_comments`, `comment_replies`, `search_videos`, `search_users`, `hashtag`, `hashtag_videos`, `user_followers`, `user_followings` | 1 each |

## Links

- [Website](https://scavio.dev)
- [Documentation](https://docs.scavio.dev)
- [Dashboard & API Keys](https://dashboard.scavio.dev)
- [API Reference](https://docs.scavio.dev/api-reference)

## License

MIT
