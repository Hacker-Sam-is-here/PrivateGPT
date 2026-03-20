# Getting Started with Private_GPT

> **Last updated:** 2026-01-24  
> **Status:** Current & maintained  
> **Target audience:** New users, developers getting started

## Quick Navigation

- [Installation](#installation)
- [Your First Chat](#your-first-chat)
- [Web Search](#web-search)
- [Image Generation](#image-generation)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

---

## Installation

### Option 1: Using pip (Standard)

```bash
# Basic installation
pip install -U private_gpt

# With OpenAI-compatible API server
pip install -U "private_gpt[api]"

# Development installation
pip install -U "private_gpt[dev]"
```

### Option 2: Using uv (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast Python package manager that Private_GPT fully supports:

```bash
# Install Private_GPT with uv
uv add private_gpt

# Or install as a global tool
uv tool install private_gpt

# Run immediately without installing
uv run private_gpt --help
```

### Option 3: Docker

```bash
# Pull and run the official Docker image
docker pull OEvortex/private_gpt:latest
docker run -it OEvortex/private_gpt:latest
```

### Verify Installation

```bash
# Check version
private_gpt version

# List available commands
private_gpt --help
```

---

## Your First Chat

### Simple Chat (No API Key Required)

Many Private_GPT providers work without authentication. Here's a quick example:

```python
from private_gpt import Meta

# Initialize the provider
ai = Meta()

# Ask a question
response = ai.chat("Explain quantum computing in simple terms")
print(response)
```

**Expected output:**
```
Quantum computing is a type of computing that uses quantum bits...
```

### Using OpenAI (With API Key)

If you have an OpenAI API key:

```python
from private_gpt import OpenAI

# Initialize with your API key
client = OpenAI(api_key="sk-your-api-key-here")

# Simple chat
response = client.chat("What are the benefits of renewable energy?")
print(response)
```

### Using Other Popular Providers

```python
# GROQ - Fast inference
from private_gpt import GROQ
groq = GROQ(api_key="your-groq-api-key")
response = groq.chat("Write a Python function to sort a list")
print(response)

# Cohere - Powerful language model
from private_gpt import Cohere
cohere = Cohere(api_key="your-cohere-api-key")
response = cohere.chat("Summarize the theory of relativity")
print(response)

# Google Gemini
from private_gpt import GEMINI
gemini = GEMINI(api_key="your-gemini-api-key")
response = gemini.chat("What is machine learning?")
print(response)
```

### Streaming Responses

For longer responses, stream them in real-time:

```python
from private_gpt import GROQ

client = GROQ(api_key="your-groq-api-key")

# Enable streaming
response = client.chat("Write a 500-word essay on AI ethics", stream=True)

# Print each chunk as it arrives
for chunk in response:
    print(chunk, end="", flush=True)
```

---

## Web Search

### DuckDuckGo Search (CLI)

```bash
# Basic text search
private_gpt text -k "python programming"

# Image search
private_gpt images -k "mountain landscape"

# News search
private_gpt news -k "AI breakthrough"

# Weather
private_gpt weather -l "New York"
```

### Search with Python

```python
from private_gpt import DuckDuckGoSearch

# Initialize
search = DuckDuckGoSearch()

# Perform text search
results = search.text("best practices for API design", max_results=5)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['link']}")
    print(f"Snippet: {result['body']}\n")
```

### Using Different Search Engines

```python
from private_gpt import BingSearch, YepSearch, YahooSearch

# Bing
bing = BingSearch()
results = bing.text("climate change solutions")

# Yep (privacy-focused)
yep = YepSearch()
results = yep.text("machine learning")

# Yahoo
yahoo = YahooSearch()
results = yahoo.text("python frameworks")
```

---

## Image Generation

### Text-to-Image Basics

```python
from private_gpt.Provider.TTI import Pollinations

# Initialize
image_generator = Pollinations()

# Generate an image
image_path = image_generator.generate_image(
    prompt="A serene mountain landscape at sunset",
    model="pollinations"
)

print(f"Image saved to: {image_path}")
```

### Using Different TTI Providers

```python
from private_gpt.Provider.TTI import Together, MiraGic

# Together AI
together = Together()
image = together.generate_image("A futuristic city")

# MiraGic
miragic = MiraGic()
image = miragic.generate_image("A robot playing chess")
```

---

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'private_gpt'"

**Solution:**
```bash
# Ensure the package is installed
pip install -U private_gpt

# Or if using uv
uv add private_gpt

# If developing locally
cd /path/to/Private_GPT
pip install -e .
```

### Issue: "API Key not valid" or "401 Unauthorized"

**Solution:**
1. Verify your API key is correct and copied without extra spaces
2. Check that your API key hasn't expired
3. Ensure you're using the correct provider class for your key

```python
# Good - API key is set correctly
client = OpenAI(api_key="sk-your-actual-key-here")

# Bad - Extra spaces or quotes
client = OpenAI(api_key=" sk-your-key ") # Extra spaces!
```

### Issue: "Rate limit exceeded" or "Too many requests"

**Solution:**
```python
import time
from private_gpt import GROQ

client = GROQ(api_key="your-api-key")

# Add delay between requests
for i in range(10):
    response = client.chat(f"Question {i}")
    print(response)
    time.sleep(2)  # Wait 2 seconds between requests
```

### Issue: Network timeout or connection errors

**Solution:**
```python
from private_gpt import OpenAI

# Increase timeout from default 30 seconds
client = OpenAI(
    api_key="your-api-key",
    timeout=60  # 60 seconds
)

try:
    response = client.chat("Your question here")
except Exception as e:
    print(f"Error: {e}")
    # Handle the error gracefully
```

### Issue: No streaming data received

**Solution:**
```python
from private_gpt import GROQ

client = GROQ(api_key="your-api-key")

# Use proper streaming syntax
response = client.chat("Write a poem", stream=True)

# Check if response is a generator
import types
if isinstance(response, types.GeneratorType):
    for chunk in response:
        print(chunk, end="", flush=True)
else:
    print(response)
```

---

## Next Steps

### 📚 Learn More

- **[API Reference](api-reference.md)** — Deep dive into all available classes and methods
- **[Provider Development](provider-development.md)** — Create custom providers
- **[Examples](examples/README.md)** — Real-world code examples
- **[Troubleshooting](troubleshooting.md)** — Solution to common problems

### 🚀 Try Advanced Features

1. **Conversational AI** — Maintain multi-turn conversations
   ```python
   from private_gpt import Meta
   
   ai = Meta(is_conversation=True)
   ai.chat("Hello, what's your name?")
   ai.chat("Can you remember my question?")  # Context preserved
   ```

2. **Web Search Integration** — Combine search with AI
   ```python
   from private_gpt import DuckDuckGoSearch, Meta
   
   search = DuckDuckGoSearch()
   results = search.text("latest AI news")
   
   ai = Meta()
   response = ai.chat(f"Summarize this news: {results[0]['body']}")
   ```

3. **CLI Interface** — Use Private_GPT from terminal
   ```bash
   private_gpt text -k "python tips and tricks"
   private_gpt images -k "nature photography" --size large
   ```

### 🔧 Customize Your Setup

- **Environment variables** — Set default API keys
- **Configuration** — Adjust timeouts, retries, and more
- **Custom providers** — Build your own integrations

---

## Command Reference

### Chat Commands

```bash
# Interactive chat (if supported by provider)
private_gpt chat

# Show available AI providers
private_gpt providers list
```

### Search Commands

```bash
# DuckDuckGo (default)
private_gpt text -k "search term"
private_gpt images -k "search term"
private_gpt news -k "search term"

# Alternative engines
private_gpt bing_text -k "search term"
private_gpt yep_text -k "search term"
private_gpt yahoo_text -k "search term"
```

### Utility Commands

```bash
# Show version
private_gpt version

# Help for specific command
private_gpt text --help
```

---

## IDE Setup

### VSCode

1. Install Python extension
2. Select your Python interpreter (where you installed Private_GPT)
3. Create a `.code-workspace` file:

```json
{
  "folders": [{"path": "."}],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
  }
}
```

### PyCharm

1. **File → Settings → Project → Python Interpreter**
2. Click the gear icon and select **Add...**
3. Choose **Existing Environment** and select your Python interpreter
4. Private_GPT should now autocomplete and provide IntelliSense

---

## Summary

You're now ready to:
- ✅ Use Private_GPT for chat and search
- ✅ Generate images
- ✅ Integrate with your projects
- ✅ Troubleshoot basic issues

**Next:** Explore the [API Reference](api-reference.md) for advanced usage patterns.

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting.md).
