# Scavio Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scavio-python.svg)](https://pypi.org/project/scavio-python/)
[![Python](https://img.shields.io/pypi/pyversions/scavio-python.svg)](https://pypi.org/project/scavio-python/)
[![Tests](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml/badge.svg)](https://github.com/scavio-ai/scavio-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the [Scavio](https://scavio.dev) Search API. Access real-time data from Google, Amazon, Walmart, YouTube, Reddit, and TikTok with a single API key. Built for AI agents, LLM applications, and data pipelines.

> Scavio is the all-in-one search API for AI -- a powerful alternative to Tavily, SerpAPI, and ScraperAPI. One API key, six data sources, structured results with knowledge graphs.

## Features

- **6 data sources** -- Google, Amazon, Walmart, YouTube, Reddit, TikTok
- **20+ endpoints** -- search, product details, video metadata, comments, profiles, and more
- **Sync + async** -- `ScavioClient` and `AsyncScavioClient` with identical APIs
- **Structured data** -- knowledge graphs, related searches, product specs out of the box
- **Built for AI** -- designed for LangChain, CrewAI, LlamaIndex, and custom agents
- **Rate limiting** -- built-in sliding-window rate limiter
- **Type hints** -- full PEP 561 support for IDE autocomplete

## Installation

```bash
pip install scavio-python
```

## Quick Start

Get your free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev).

```python
from scavio import ScavioClient

client = ScavioClient(api_key="sk_...")  # or set SCAVIO_API_KEY env var

results = client.search("best noise cancelling headphones 2026")
print(results["results"])
```

## Usage

### Google Search

```python
# Basic search
results = client.search("pizza new york", country_code="us", language="en")

# News search
news = client.google.search("AI startups", search_type="news")

# Image search
images = client.google.search("sunset wallpaper", search_type="images")
```

### Amazon

```python
# Search products
products = client.amazon.search("wireless headphones", domain="com", sort_by="most_recent")

# Get product details by ASIN
product = client.amazon.product("B09V3KXJPB")
```

### Walmart

```python
products = client.walmart.search("wireless headphones", sort_by="best_match")

product = client.walmart.product("123456789")
```

### YouTube

```python
videos = client.youtube.search("javascript tutorial", sort_by="view_count")

metadata = client.youtube.metadata("dQw4w9WgXcQ")
```

### Reddit

```python
posts = client.reddit.search("python web scraping", sort="hot")

post = client.reddit.post("https://www.reddit.com/r/programming/comments/abc123/example/")
```

### TikTok

```python
profile = client.tiktok.profile(username="tiktok")

videos = client.tiktok.search_videos("cooking recipe", count=10)

video = client.tiktok.video("7000000000000000000")

comments = client.tiktok.video_comments("7000000000000000000")
```

### Check Usage

```python
usage = client.get_usage()
print(f"Plan: {usage['plan']}, Credits: {usage['credit_balance']}")
```

## Async Support

```python
import asyncio
from scavio import AsyncScavioClient

async def main():
    async with AsyncScavioClient(api_key="sk_...") as client:
        results = await client.search("best restaurants in NYC")
        print(results)

asyncio.run(main())
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
