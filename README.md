# Scavio Python SDK

Python SDK for the [Scavio](https://scavio.dev) Search API. Access real-time data from Google, Amazon, Walmart, YouTube, Reddit, and TikTok with a single API key.

## Installation

```bash
pip install scavio-python
```

## Quick Start

```python
from scavio import ScavioClient

client = ScavioClient(api_key="sk_...")  # or set SCAVIO_API_KEY env var

results = client.search("best noise cancelling headphones")
print(results)
```

## Usage

### Google Search

```python
results = client.search("pizza new york", country_code="us", language="en")

# Or use the namespace
results = client.google.search("pizza new york", search_type="news")
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
print(usage["credit_balance"])
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
from scavio import ScavioClient, InvalidAPIKeyError, RateLimitError, InsufficientCreditsError

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

## Links

- [Documentation](https://docs.scavio.dev)
- [Dashboard](https://dashboard.scavio.dev)
- [API Reference](https://docs.scavio.dev/api-reference)

## License

MIT
