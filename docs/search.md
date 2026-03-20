# 🔍 Private_GPT Search Module
> Last updated: 2025-12-20
> Maintained by [Private_GPT](https://github.com/OEvortex/Private_GPT)

Private_GPT's Search module provides comprehensive access to multiple search engines through a unified, easy-to-use API. The module supports various search engines including DuckDuckGo, Yep, Bing, Yahoo, Brave, Mojeek, Yandex, Wikipedia, and more. For CLI usage, see [docs/cli.md](cli.md); the commands there call the same classes documented below.

## Table of Contents

1. [Core Components](#core-components)
2. [Quick Start](#quick-start)
3. [Search Engines](#search-engines)
4. [Individual Search Engines](#individual-search-engines)
5. [Command Line Interface](#command-line-interface)
6. [Advanced Usage](#advanced-usage)
7. [API Reference](#api-reference)
8. [Integration Guide](#integration-guide)

## Core Components

### [`search/__init__.py`](../private_gpt/search/__init__.py:1)

The main search module that provides unified access to all search engines.

```python
from private_gpt.search import (
    DuckDuckGoSearch, 
    YepSearch, 
    BingSearch, 
    YahooSearch,
    Brave, 
    Mojeek, 
    Yandex, 
    Wikipedia,
    TextResult, 
    ImagesResult, 
    VideosResult, 
    NewsResult, 
    BooksResult
)

# Core search interfaces
ddg = DuckDuckGoSearch()
yep = YepSearch()
bing = BingSearch()
yahoo = YahooSearch()

# Specialized engines
brave = Brave()
mojeek = Mojeek()
yandex = Yandex()
wiki = Wikipedia()
```

**Key Features:**
- Unified interface for multiple search engines
- Comprehensive search types (text, images, videos, news, etc.)
- Advanced filtering and parameter support
- Result data classes for type safety
- Context manager support for resource management
- Error handling and rate limiting

### [`search/base.py`](../private_gpt/search/base.py:1)

Base classes for search engine implementations.

```python
from private_gpt.search.base import BaseSearch, BaseSearchEngine

# BaseSearch: Unified interface for search engines
# BaseSearchEngine: Abstract base class for engine implementations
```

### [`search/results.py`](../private_gpt/search/results.py:1)

Data classes for search results with type safety.

```python
from private_gpt.search.results import TextResult, ImagesResult, VideosResult, NewsResult, BooksResult

# TextResult: Text search results
# ImagesResult: Image search results
# VideosResult: Video search results
# NewsResult: News search results
# BooksResult: Book search results
```

## Quick Start

```python
from private_gpt.search import DuckDuckGoSearch, YepSearch

# DuckDuckGo Search
ddg = DuckDuckGoSearch()
results = ddg.text("python programming", max_results=5)

# Yep Search
yep = YepSearch()
results = yep.text("web development", max_results=5)

# Display results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['href']}")
    print(f"Description: {result['body']}")
```

## Search Engines

### DuckDuckGo Search (DuckDuckGoSearch)

DuckDuckGo offers privacy-focused search with comprehensive features across multiple categories.

#### Features
- **Privacy-focused**: No tracking or personalized results
- **Comprehensive search types**: Text, images, videos, news, maps, translations, suggestions, weather
- **Advanced filtering**: Region, SafeSearch, time limits
- **Context manager support**: Proper resource management

#### Basic Usage

```python
from private_gpt.search import DuckDuckGoSearch

# Initialize DuckDuckGo search
ddg = DuckDuckGoSearch()

# Simple text search
results = ddg.text("python programming", max_results=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['href']}")
    print(f"Description: {result['body']}")
```

#### Available Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `text()` | General web search | `keywords`, `region`, `safesearch`, `timelimit`, `backend`, `max_results` |
| `answers()` | Instant answers | `keywords` |
| `images()` | Image search | `keywords`, `region`, `safesearch`, `timelimit`, `size`, `color`, `type_image`, `layout`, `license_image`, `max_results` |
| `videos()` | Video search | `keywords`, `region`, `safesearch`, `timelimit`, `resolution`, `duration`, `license_videos`, `max_results` |
| `news()` | News articles | `keywords`, `region`, `safesearch`, `timelimit`, `max_results` |
| `maps()` | Location search | `keywords`, `place`, `street`, `city`, `county`, `state`, `country`, `postalcode`, `latitude`, `longitude`, `radius`, `max_results` |
| `translate()` | Text translation | `keywords`, `from_lang`, `to_lang` |
| `suggestions()` | Search suggestions | `keywords`, `region` |
| `weather()` | Weather information | `keywords` |

#### Advanced Examples

##### Text Search with Filters

```python
results = ddg.text(
    keywords="artificial intelligence",
    region="wt-wt",           # Region code
    safesearch="moderate",    # "on", "moderate", "off"
    timelimit="y",            # "d"=day, "w"=week, "m"=month, "y"=year
    backend="api",           # "api" or "html"
    max_results=10
)
```

##### News Search

```python
news_results = ddg.news(
    keywords="technology trends",
    region="wt-wt",
    safesearch="moderate",
    timelimit="w",  # Last week
    max_results=20
)

for item in news_results:
    print(f"Title: {item['title']}")
    print(f"Date: {item['date']}")
    print(f"Source: {item['url']}")
    print(f"Summary: {item['body']}")
```

##### Weather Information

```python
weather = ddg.weather("New York")
if weather:
    print(f"Location: {weather['location']}")
    print(f"Temperature: {weather['current']['temperature_c']}°C")
    print(f"Condition: {weather['current']['condition']}")
```

##### Maps Search

```python
maps_results = ddg.maps(
    keywords="restaurants",
    place="new york",
    max_results=30
)
```

##### Image Search with Advanced Filters

```python
image_results = ddg.images(
    keywords="nature photography",
    region="wt-wt",
    safesearch="moderate",
    timelimit="m",  # Last month
    size="large",  # "small", "medium", "large", "wallpaper"
    color="green", # Color filter
    type_image="photo",  # "photo", "clipart", "line", "animated", "face"
    layout="square",  # "square", "tall", "wide"
    license_image="commercial",  # License filter
    max_results=50
)
```

##### Video Search with Filters

```python
video_results = ddg.videos(
    keywords="python tutorials",
    region="wt-wt",
    safesearch="moderate",
    timelimit="y",  # Last year
    resolution="hd",  # "sd", "hd"
    duration="medium",  # "short", "medium", "long"
    license_videos="creativeCommon",  # License filter
    max_results=30
)
```

### Yep Search (YepSearch)

Yep.com provides fast, privacy-focused search results with a clean interface and multiple content types.

#### Features
- **Privacy-focused**: Alternative to mainstream search engines
- **Fast responses**: Optimized for speed
- **Multiple content types**: Text and images
- **Search suggestions**: Autocomplete functionality

#### Basic Usage

```python
from private_gpt.search import YepSearch

# Initialize YepSearch
yep = YepSearch()

# Text Search
text_results = yep.text(
    keywords="artificial intelligence",
    region="all",           # Optional: Region for results
    safesearch="moderate",  # Optional: "on", "moderate", "off"
    max_results=10          # Optional: Limit number of results
)

for result in text_results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['href']}")
    print(f"Description: {result['body']}")
```

#### Available Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `text()` | Text search | `keywords`, `region`, `safesearch`, `max_results` |
| `images()` | Image search | `keywords`, `region`, `safesearch`, `max_results` |
| `suggestions()` | Search suggestions | `query`, `region` |

#### Image Search Example

```python
image_results = yep.images(
    keywords="nature photography",
    region="all",
    safesearch="moderate",
    max_results=10
)

for image in image_results:
    print(f"Title: {image['title']}")
    print(f"URL: {image['image']}")
    print(f"Thumbnail: {image['thumbnail']}")
```

## Individual Search Engines

Private_GPT also provides direct access to individual search engines for specialized use cases.

### Available Engines

| Engine | Description | Features |
|--------|-------------|----------|
| `BingSearch` | Microsoft's search engine | Text search, news, images, suggestions |
| `Brave` | Privacy-focused modern search | Text search, high-quality results |
| `Mojeek` | Independent European search engine | Text search, privacy-first |
| `YahooSearch` | Yahoo search | Text search, news, images, videos, maps, translations, weather |
| `Yandex` | Global search engine (Yandex) | Text search, robust parsing |
| `Wikipedia` | Encyclopedia search | Article summaries, links |
| `DuckDuckGoSearch`| Privacy-focused search | Comprehensive (Text, Images, News, etc.) |
| `YepSearch` | Fast, privacy-focused search | Text and Images |

### Usage Examples

```python
from private_gpt.search import BingSearch, Brave, YahooSearch, Yandex, Wikipedia
from private_gpt.search.engines.bing.news import BingNews
from private_gpt.search.engines.yahoo.news import YahooNews

# Bing Search
bing = BingSearch()
results = bing.search("python programming", max_results=10)

# Brave Search
brave = Brave()
results = brave.search("artificial intelligence", max_results=10)

# Yahoo Search
yahoo = YahooSearch()
results = yahoo.search("web development", max_results=10)

# Yandex Search
yandex = Yandex()
results = yandex.search("machine learning", max_results=10)

# Wikipedia Search
wiki = Wikipedia()
results = wiki.search("quantum computing", max_results=5)

# News-specific engines
bing_news = BingNews()
news_results = bing_news.search("technology news", max_results=15)

yahoo_news = YahooNews()
news_results = yahoo_news.search("AI breakthroughs", max_results=15)
```

### Bing Search Engine

```python
from private_gpt.search import BingSearch
from private_gpt.search.engines.bing.text import BingTextSearch
from private_gpt.search.engines.bing.images import BingImages
from private_gpt.search.engines.bing.news import BingNews
from private_gpt.search.engines.bing.suggestions import BingSuggestions

# Unified Bing interface
bing = BingSearch()
text_results = bing.search("python programming", max_results=10)

# Direct engine access
text_engine = BingTextSearch()
text_results = text_engine.run("python programming", max_results=10)

image_engine = BingImages()
image_results = image_engine.run("nature photography", max_results=20)

news_engine = BingNews()
news_results = news_engine.run("technology news", max_results=15)

suggestions_engine = BingSuggestions()
suggestions = suggestions_engine.run("how to learn")
```

### Yahoo Search Engine

```python
from private_gpt.search import YahooSearch
from private_gpt.search.engines.yahoo.text import YahooTextSearch
from private_gpt.search.engines.yahoo.images import YahooImages
from private_gpt.search.engines.yahoo.news import YahooNews
from private_gpt.search.engines.yahoo.videos import YahooVideos
from private_gpt.search.engines.yahoo.maps import YahooMaps
from private_gpt.search.engines.yahoo.translate import YahooTranslate
from private_gpt.search.engines.yahoo.weather import YahooWeather

# Unified Yahoo interface
yahoo = YahooSearch()
text_results = yahoo.search("web development", max_results=10)

# Direct engine access
text_engine = YahooTextSearch()
text_results = text_engine.run("web development", region="us", max_results=10)

image_engine = YahooImages()
image_results = image_engine.run("landscapes", region="us", max_results=20)

news_engine = YahooNews()
news_results = news_engine.run("AI news", region="us", max_results=15)

video_engine = YahooVideos()
video_results = video_engine.run("python tutorials", region="us", max_results=10)

maps_engine = YahooMaps()
maps_results = maps_engine.run("restaurants", city="New York", max_results=30)

translate_engine = YahooTranslate()
translation = translate_engine.run("hello world", from_lang="en", to_lang="es")

weather_engine = YahooWeather()
weather = weather_engine.run("New York")
```

### Brave Search (Brave)
Brave search is a modern, privacy-focused search engine that doesn't track you.

```python
from private_gpt.search import Brave

brave = Brave()
results = brave.run("artificial intelligence", max_results=5)
for result in results:
    print(f"{result.title}: {result.href}")
```

### Mojeek Search (Mojeek)
Mojeek is an independent, privacy-first search engine based in Europe.

```python
from private_gpt.search import Mojeek

mojeek = Mojeek()
results = mojeek.run("privacy tools", max_results=5)
```

### Yandex Search (Yandex)
Yandex provides global search results with strong parsing capabilities.

```python
from private_gpt.search import Yandex

yandex = Yandex()
results = yandex.run("python tutorials", max_results=5)
```

### Wikipedia Search (Wikipedia)
Access Wikipedia article summaries and links directly.

```python
from private_gpt.search import Wikipedia

wiki = Wikipedia()
# Region parameter determines the language (e.g., 'en-us' for English)
results = wiki.run("Quantum Computing", region="en-us", max_results=3)
```

## Command Line Interface

Private_GPT provides a simple, unified CLI for all search engines. Use the generic commands (`text`, `images`, `news`, etc.) and the `--engine` (or `-e`) flag to select your provider.

### Basic Examples

```bash
# General text search (default engine: ddg)
private_gpt text -k "python programming" -m 10

# Search using a specific engine
private_gpt text -k "artificial intelligence" -e brave

# Image search on Bing
private_gpt images -k "cyberpunk landscape" -e bing

# News search on Yahoo
private_gpt news -k "space exploration" -e yahoo

# Get suggestions from Yep
private_gpt suggestions -q "world cup" -e yep

# Weather info via Yahoo
private_gpt weather -l "London" -e yahoo
```

### Unified Search Shortcut
The `search` command is a shortcut for the `text` command:
```bash
private_gpt search -k "quantum computing" -e wikipedia
```

## Advanced Usage

### Asynchronous Search

```python
import asyncio
from private_gpt.search import DuckDuckGoSearch

async def search_multiple_terms(search_terms):
    async with DuckDuckGoSearch() as ddg:
        # Create tasks for each search term
        tasks = [ddg.text(term, max_results=5) for term in search_terms]
        # Run all searches concurrently
        results = await asyncio.gather(*tasks)
        return results

async def main():
    terms = ["python", "javascript", "machine learning"]
    all_results = await search_multiple_terms(terms)

    # Process results
    for i, term_results in enumerate(all_results):
        print(f"Results for '{terms[i]}':")
        for result in term_results:
            print(f"- {result['title']}")
        print()

# Run the async function
asyncio.run(main())
```

### Custom Configuration

```python
from private_gpt.search import DuckDuckGoSearch

# Note: DuckDuckGoSearch() doesn't accept constructor arguments
# Proxy and timeout configuration is handled internally
# For custom configuration, use the individual engine classes

ddg = DuckDuckGoSearch()
results = ddg.text("search query", max_results=10)
```

### Error Handling

```python
from private_gpt.search import DuckDuckGoSearch
from private_gpt.exceptions import Private_GPTE

try:
    ddg = DuckDuckGoSearch()
    results = ddg.text("python programming", max_results=5)
    print(f"Found {len(results)} results")
except Private_GPTE as e:
    print(f"Search failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Result Processing

```python
from private_gpt.search import DuckDuckGoSearch
import json

ddg = DuckDuckGoSearch()

# Get results
results = ddg.text("artificial intelligence", max_results=10)

# Convert to different formats
# As JSON
json_results = json.dumps(results, indent=2)

# Extract URLs only
urls = [result['href'] for result in results]

# Filter results
filtered_results = [
    result for result in results
    if 'python' in result['title'].lower()
]

# Save to file
with open('search_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Using Result Data Classes

```python
from private_gpt.search import DuckDuckGoSearch
from private_gpt.search.results import TextResult, ImagesResult

# Get text results
ddg = DuckDuckGoSearch()
text_results = ddg.text("python programming", max_results=5)

# Convert to TextResult objects
text_objects = [TextResult(**result) for result in text_results]

# Access typed properties
for result in text_objects:
    print(f"Title: {result.title}")
    print(f"URL: {result.href}")
    print(f"Description: {result.body}")
    print(f"As dict: {result.to_dict()}")

# Get image results
image_results = ddg.images("nature photography", max_results=5)
image_objects = [ImagesResult(**result) for result in image_results]

# Access image properties
for image in image_objects:
    print(f"Title: {image.title}")
    print(f"Image URL: {image.image}")
    print(f"Thumbnail: {image.thumbnail}")
    print(f"Dimensions: {image.width}x{image.height}")
```

### Multi-Engine Search

```python
from private_gpt.search import DuckDuckGoSearch, YepSearch, BingSearch

def search_all_engines(query, max_results=5):
    """Search using multiple engines and combine results"""
    
    # Initialize engines
    ddg = DuckDuckGoSearch()
    yep = YepSearch()
    bing = BingSearch()
    
    # Perform searches
    ddg_results = ddg.text(query, max_results=max_results)
    yep_results = yep.text(query, max_results=max_results)
    bing_results = bing.search(query, max_results=max_results)
    
    # Combine and deduplicate results
    all_results = []
    seen_urls = set()
    
    for results in [ddg_results, yep_results, bing_results]:
        for result in results:
            if result['href'] not in seen_urls:
                all_results.append(result)
                seen_urls.add(result['href'])
    
    return all_results

# Example usage
results = search_all_engines("python programming", max_results=5)
print(f"Found {len(results)} unique results from multiple engines")

for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']} - {result['href']}")
```

## API Reference

### DuckDuckGoSearch Class

#### Constructor

```python
DuckDuckGoSearch()
```

**Note:** The DuckDuckGoSearch class does not accept constructor parameters. Configuration like timeout, proxies, and SSL verification are handled internally by the underlying search engine implementations.

#### Methods

##### text(keywords, region="wt-wt", safesearch="moderate", timelimit=None, backend="api", max_results=None)

Performs a general web search.

**Parameters:**
- `keywords` (str): Search query
- `region` (str): Region code (default: "wt-wt")
- `safesearch` (str): SafeSearch level ("on", "moderate", "off")
- `timelimit` (str): Time limit ("d", "w", "m", "y")
- `backend` (str): Backend to use ("api" or "html")
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

##### answers(keywords)

Gets instant answers for a query.

**Parameters:**
- `keywords` (str): Search query

**Returns:** List of answer dictionaries

##### images(keywords, region="wt-wt", safesearch="moderate", timelimit=None, size=None, color=None, type_image=None, layout=None, license_image=None, max_results=None)

Searches for images.

**Parameters:**
- `keywords` (str): Search query
- `region` (str): Region code
- `safesearch` (str): SafeSearch level
- `timelimit` (str): Time limit
- `size` (str): Image size ("small", "medium", "large", "wallpaper")
- `color` (str): Color filter
- `type_image` (str): Image type ("photo", "clipart", "line", "animated", "face")
- `layout` (str): Layout ("square", "tall", "wide")
- `license_image` (str): License filter
- `max_results` (int): Maximum results

**Returns:** List of image result dictionaries

##### videos(keywords, region="wt-wt", safesearch="moderate", timelimit=None, resolution=None, duration=None, license_videos=None, max_results=None)

Searches for videos.

**Parameters:**
- Similar to images() with video-specific filters
- `resolution` (str): Video resolution ("sd", "hd")
- `duration` (str): Video duration ("short", "medium", "long")
- `license_videos` (str): Video license filter

**Returns:** List of video result dictionaries

##### news(keywords, region="wt-wt", safesearch="moderate", timelimit=None, max_results=None)

Searches for news articles.

**Parameters:**
- Similar to text()

**Returns:** List of news result dictionaries

##### maps(keywords, place=None, street=None, city=None, county=None, state=None, country=None, postalcode=None, latitude=None, longitude=None, radius=0, max_results=None)

Searches for locations and places.

**Parameters:**
- `keywords` (str): Search query
- `place` (str): Place name
- `street` (str): Street address
- `city` (str): City name
- `county` (str): County name
- `state` (str): State name
- `country` (str): Country name
- `postalcode` (str): Postal code
- `latitude` (float): Latitude coordinate
- `longitude` (float): Longitude coordinate
- `radius` (int): Search radius in kilometers
- `max_results` (int): Maximum results

**Returns:** List of map result dictionaries

##### translate(keywords, from_lang=None, to_lang="en")

Translates text between languages.

**Parameters:**
- `keywords` (str): Text to translate
- `from_lang` (str): Source language (auto-detected if None)
- `to_lang` (str): Target language (default: "en")

**Returns:** List of translation result dictionaries

##### suggestions(keywords, region="wt-wt")

Gets search suggestions.

**Parameters:**
- `keywords` (str): Partial search query
- `region` (str): Region code

**Returns:** List of suggestion strings

##### weather(keywords)

Gets weather information for a location.

**Parameters:**
- `keywords` (str): Location name

**Returns:** Weather data dictionary

### YepSearch Class

#### Constructor

```python
YepSearch()
```

**Note:** The YepSearch class does not accept constructor parameters. Configuration like timeout, proxies, and SSL verification are handled internally by the underlying search engine implementations.

#### Methods

##### text(keywords, region="all", safesearch="moderate", max_results=None)

##### images(keywords, region="all", safesearch="moderate", max_results=None)

##### suggestions(query, region="all")

### BingSearch Class

#### Constructor

```python
BingSearch()
```

#### Methods

##### search(keywords, max_results=None)

Performs Bing text search.

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

### YahooSearch Class

#### Constructor

```python
YahooSearch()
```

#### Methods

##### search(keywords, region="us", max_results=None)

Performs Yahoo text search.

**Parameters:**
- `keywords` (str): Search query
- `region` (str): Region code (default: "us")
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

### Brave Class

#### Constructor

```python
Brave()
```

#### Methods

##### search(keywords, max_results=None)

Performs Brave text search.

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

### Mojeek Class

#### Constructor

```python
Mojeek()
```

#### Methods

##### search(keywords, max_results=None)

Performs Mojeek text search.

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

### Yandex Class

#### Constructor

```python
Yandex()
```

#### Methods

##### search(keywords, max_results=None)

Performs Yandex text search.

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

### Wikipedia Class

#### Constructor

```python
Wikipedia()
```

#### Methods

##### search(keywords, max_results=None)

Performs Wikipedia article search.

**Parameters:**
- `keywords` (str): Search query
- `max_results` (int): Maximum results to return

**Returns:** List of result dictionaries

## Integration Guide

### With Private_GPT Providers

```python
from private_gpt.search import DuckDuckGoSearch
from private_gpt.Provider import ChatGPT

# Get search results
ddg = DuckDuckGoSearch()
search_results = ddg.text("latest AI research", max_results=5)

# Use with AI provider
chatgpt = ChatGPT()
response = chatgpt.ask(f"Summarize these search results: {search_results}")
print(response)
```

### With FastAPI

```python
from fastapi import FastAPI, HTTPException
from private_gpt.search import DuckDuckGoSearch, YepSearch

app = FastAPI()

@app.get("/search")
async def search(query: str, engine: str = "duckduckgo", max_results: int = 10):
    """Search using specified engine"""
    try:
        if engine == "duckduckgo":
            search_engine = DuckDuckGoSearch()
            results = search_engine.text(query, max_results=max_results)
        elif engine == "yep":
            search_engine = YepSearch()
            results = search_engine.text(query, max_results=max_results)
        else:
            raise HTTPException(status_code=400, detail="Unsupported search engine")
        
        return {
            "query": query,
            "engine": engine,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### With Async Applications

```python
import asyncio
from private_gpt.search import DuckDuckGoSearch

async def search_and_process(query: str):
    """Search and process results asynchronously"""
    async with DuckDuckGoSearch() as ddg:
        # Perform search
        results = await asyncio.to_thread(ddg.text, query, max_results=10)
        
        # Process results
        processed = []
        for result in results:
            processed.append({
                "title": result["title"],
                "url": result["href"],
                "summary": result["body"][:100] + "..." if len(result["body"]) > 100 else result["body"]
            })
        
        return processed

async def main():
    queries = ["python programming", "machine learning", "web development"]
    
    # Run multiple searches concurrently
    tasks = [search_and_process(query) for query in queries]
    all_results = await asyncio.gather(*tasks)
    
    for i, results in enumerate(all_results):
        print(f"Results for '{queries[i]}': {len(results)} found")

# Run the async function
asyncio.run(main())
```

### With Data Analysis

```python
import pandas as pd
from private_gpt.search import DuckDuckGoSearch

# Get search results
ddg = DuckDuckGoSearch()
results = ddg.text("python programming tutorials", max_results=20)

# Convert to DataFrame
df = pd.DataFrame(results)

# Analyze results
print(f"Total results: {len(df)}")
print(f"\nTop domains:")
df['href'].str.extract(r'https?://([^/]+)')[0].value_counts().head(5)

# Filter results
python_results = df[df['title'].str.contains('Python', case=False, na=False)]
print(f"\nResults containing 'Python': {len(python_results)}")

# Save to CSV
df.to_csv('search_results.csv', index=False)
```

### With CLI Applications

```python
import click
from private_gpt.search import DuckDuckGoSearch, YepSearch

@click.group()
def cli():
    """Private_GPT Search CLI"""
    pass

@cli.command()
@click.argument('query')
@click.option('--engine', '-e', default='duckduckgo', help='Search engine (duckduckgo/yep)')
@click.option('--max-results', '-m', default=10, help='Maximum results')
def search(query, engine, max_results):
    """Search using specified engine"""
    try:
        if engine == 'duckduckgo':
            search_engine = DuckDuckGoSearch()
        elif engine == 'yep':
            search_engine = YepSearch()
        else:
            click.echo(f"Unsupported engine: {engine}", err=True)
            return
        
        results = search_engine.text(query, max_results=max_results)
        
        click.echo(f"Found {len(results)} results for '{query}':")
        for i, result in enumerate(results, 1):
            click.echo(f"{i}. {result['title']}")
            click.echo(f"   {result['href']}")
            click.echo(f"   {result['body'][:100]}...")
            click.echo()
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    cli()
```

### With Web Applications

```python
from flask import Flask, request, render_template
from private_gpt.search import DuckDuckGoSearch

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        max_results = int(request.form.get('max_results', 10))
        
        try:
            ddg = DuckDuckGoSearch()
            results = ddg.text(query, max_results=max_results)
            return render_template('results.html', 
                                 query=query, 
                                 results=results, 
                                 count=len(results))
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## Usage Tips

> [!TIP]
> - **Handle Errors Gracefully**: Always implement proper error handling for production use
> - **Set Reasonable Limits**: Don't request excessive results; most engines limit responses
> - **Respect Rate Limits**: Add delays between multiple requests
> - **Cache Results**: Cache search results when possible to reduce API calls
> - **Use Appropriate Result Limits**: Start with smaller `max_results` values and increase as needed
> - **Context Managers**: Use `async with` for asynchronous operations to ensure proper resource cleanup
> - **Result Processing**: Use the provided data classes for type-safe result handling
> - **Multi-Engine Search**: Combine results from multiple engines for comprehensive coverage

## Configuration Best Practices

```python
# For production use with error handling
from private_gpt.search import DuckDuckGoSearch
from private_gpt.exceptions import Private_GPTE
import time

def safe_search(query, max_retries=3, retry_delay=5):
    """Safe search with retry logic"""
    for attempt in range(max_retries):
        try:
            ddg = DuckDuckGoSearch()
            results = ddg.text(query, max_results=10)
            return results
        except Private_GPTE as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

# Example usage
try:
    results = safe_search("python programming")
    print(f"Found {len(results)} results")
except Exception as e:
    print(f"Search failed after retries: {e}")
```

## Advanced Features

### Custom Search Engines

```python
from private_gpt.search.base import BaseSearchEngine
from private_gpt.search.results import TextResult

class CustomSearchEngine(BaseSearchEngine):
    """Custom search engine implementation"""
    
    name = "custom"
    category = "text"
    provider = "custom"
    search_url = "https://custom-search.example.com/search"
    search_method = "GET"
    items_xpath = "//div[@class='result']"
    elements_xpath = {
        "title": ".//h3/a/text()",
        "href": ".//h3/a/@href",
        "body": ".//p[@class='description']/text()"
    }
    
    def run(self, query: str, **kwargs):
        """Run the search"""
        # Implement custom search logic
        # Use self.http_client to make requests
        # Parse results and return as list of dicts
        results = []
        # ... custom implementation ...
        return results

# Register the custom engine
from private_gpt.search import BaseSearch

class CustomSearch(BaseSearch):
    def __init__(self):
        super().__init__()
        self.text_engine = CustomSearchEngine()
    
    def search(self, query, **kwargs):
        return self.text_engine.run(query, **kwargs)

# Usage
custom = CustomSearch()
results = custom.search("test query")
```

### Search Result Processing Pipeline

```python
from private_gpt.search import DuckDuckGoSearch
from private_gpt.sanitize import sanitize_stream

def process_search_results(query, max_results=10):
    """Complete search and processing pipeline"""
    
    # Step 1: Perform search
    ddg = DuckDuckGoSearch()
    results = ddg.text(query, max_results=max_results)
    
    # Step 2: Clean and filter results
    cleaned_results = []
    for result in results:
        # Clean text content
        clean_content = list(sanitize_stream(
            result['body'],
            intro_value="",
            to_json=False,
            strip_chars="\n\r\t"
        ))
        
        # Reconstruct result with cleaned content
        cleaned_result = {
            'title': result['title'],
            'href': result['href'],
            'body': ' '.join(clean_content)
        }
        cleaned_results.append(cleaned_result)
    
    # Step 3: Filter and sort
    filtered_results = [
        r for r in cleaned_results 
        if len(r['body'].split()) > 10  # Minimum words
    ]
    
    # Sort by title length (example)
    sorted_results = sorted(filtered_results, key=lambda x: len(x['title']), reverse=True)
    
    return sorted_results

# Example usage
results = process_search_results("python programming", max_results=15)
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
    print(f"   {result['body'][:150]}...")
```

### Search with Private_GPT Sanitization

```python
from private_gpt.search import DuckDuckGoSearch
from private_gpt.sanitize import sanitize_stream, lit_streamer

# Use sanitize_stream decorator for search results
@lit_streamer(to_json=False, strip_chars="\n\r\t")
def clean_search_result(result):
    """Clean a single search result"""
    yield result['title']
    yield result['href']
    yield result['body']

# Perform search and clean results
ddg = DuckDuckGoSearch()
raw_results = ddg.text("python programming", max_results=5)

# Process each result
for result in raw_results:
    cleaned = list(clean_search_result(result))
    print(f"Title: {cleaned[0]}")
    print(f"URL: {cleaned[1]}")
    print(f"Body: {cleaned[2][:100]}...")
```

## Troubleshooting

### Common Issues

1. **Timeout Errors**
   ```python
   # Timeout is handled internally by the search engine implementation
   # If experiencing timeout issues, try reducing max_results
   ddg = DuckDuckGoSearch()
   results = ddg.text("query", max_results=5)
   ```

2. **Rate Limiting**
   ```python
   # Add delays between requests
   import time
   results = ddg.text("query", max_results=5)
   time.sleep(1)  # Wait 1 second between requests
   ```

3. **Network Issues**
   ```python
   # Handle network-related exceptions
   from private_gpt.exceptions import Private_GPTE
   try:
       results = ddg.text("query", max_results=5)
   except Private_GPTE as e:
       print(f"Search failed: {e}")
   ```

### Error Types

- `Private_GPTE`: Base Private_GPT exception
- `RatelimitE`: Rate limit exceeded
- `TimeoutE`: Request timeout
- Standard Python exceptions for network/connectivity issues

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Perform search with debug output
ddg = DuckDuckGoSearch()
results = ddg.text("test query", max_results=3)
```

## Best Practices

1. **Handle Errors Gracefully**: Always implement proper error handling for production use
2. **Set Reasonable Limits**: Don't request excessive results; most engines limit responses
3. **Respect Rate Limits**: Add delays between multiple requests
4. **Cache Results**: Cache search results when possible to reduce API calls
5. **Use Appropriate Result Limits**: Start with smaller `max_results` values and increase as needed
6. **Context Managers**: Use `async with` for asynchronous operations
7. **Result Processing**: Use the provided data classes for type safety
8. **Multi-Engine Search**: Combine results from multiple engines for better coverage
9. **Query Optimization**: Use specific keywords and filters to get better results
10. **Result Validation**: Validate and clean search results before using them

## Contributing

To add support for new search engines:

1. Create a new engine class in `private_gpt/search/engines/`
2. Implement the required interface methods
3. Add the engine to `private_gpt/search/__init__.py`
4. Update this documentation
5. Add CLI commands if appropriate

## License

This search functionality is part of Private_GPT and follows the same license terms.

<div align="center">
  <p>
    <a href="https://github.com/OEvortex/Private_GPT"><img alt="GitHub Repository" src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white"></a>
    <a href="https://t.me/PyscoutAI"><img alt="Telegram Group" src="https://img.shields.io/badge/Telegram%20Group-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  </p>
</div>

*This documentation covers the comprehensive functionality of the [`private_gpt.search`](../private_gpt/search/__init__.py:1) module. For the most up-to-date information, refer to the source code and inline documentation.*
