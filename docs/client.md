# Private_GPT Python API Client (`private_gpt/client.py`)
> Last updated: 2025-12-20
> Maintained by: Private_GPT Core Team

The Private_GPT Python API Client is a Python-based client library that provides OpenAI-compatible API access to any provider within the Private_GPT ecosystem. It allows you to use any Private_GPT provider with models formatted in OpenAI-compatible format, making it easy to integrate with existing OpenAI-based applications. The client handles provider discovery, model lookup, automatic failover, and streaming so you can focus on your application logic rather than provider-specific plumbing.

## ✨ Highlights

- **Python-native API**: A pure Python client library for Private_GPT providers using OpenAI-compatible format.
- **Auto-discovery** of OpenAI-compatible (`private_gpt/Provider/OPENAI`) and TTI (`private_gpt/Provider/TTI`) providers via dynamic imports.
- **Smart model resolution** supporting explicit provider/model pairs (`Provider/model`), fuzzy matches, and `auto` selection.
- **Intelligent Auto-resolution**: `model="auto"` selects a random provider that advertises models via `models.list()`, with fallback to default models.
- **Automatic failover**: retries across compatible providers when a request fails or returns empty content, organized in three-tiered strategy:
  - Tier 1: Providers that advertise the exact model name
  - Tier 2: Providers with fuzzy-matched model names using `difflib.get_close_matches`
  - Tier 3: Remaining providers with random model selection
- **Streaming support**: yields `ChatCompletionChunk` objects with OpenAI-compatible format, preserving provider metadata.
- **Unified caching**: provider instances are cached per process to avoid repeated authentication or setup cost.
- **OpenAI-compatible responses**: all responses follow OpenAI API format for easy integration.
- **Image generation**: supports OpenAI-compatible Images API with consistent response objects.

## 🚀 Quick Start

```python
from private_gpt.client import Client

client = Client(print_provider_info=True)

# Chat completion with automatic provider+model selection
resp = client.chat.completions.create(
    model="auto",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the benefits of Private_GPT."}
    ],
)
print(resp.choices[0].message.content)

# Streaming response
stream = client.chat.completions.create(
    model="ChatGPT/gpt-4o-mini",  # Provider/model pair
    messages=[{"role": "user", "content": "Write a limerick about Python."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)

# Image generation (TTI)
img = client.images.generate(
    prompt="A neon cyberpunk owl overlooking a futuristic city",
    model="auto",
    size="1024x1024",
)
print(img.data[0].url)
```

## 🧠 Provider & Model Resolution

- **Explicit pair**: `MODEL="ProviderName/model-id"` chooses an exact provider class and model.
- **Provider override**: pass `provider=<ProviderClass>` to force a class while leaving `model` as "auto" or a specific value.
- **Auto resolution for chat**: `model="auto"` selects a random provider with available models, raising an error if no models are available.
- **Auto resolution for images**: `model="auto"` selects a random provider with available models, raising an error if no models are available.
- **Fuzzy matching**: if a model name isn't found, `_fuzzy_resolve_provider_and_model` uses:
  1. Exact case-insensitive matching
  2. Substring matching (model name contained in or contains available model name)
  3. `difflib.get_close_matches` with 0.5 cutoff score
- **Fallback queue**: if the chosen provider fails, the client tries three tiers:
  1. Providers that advertise the exact model name
  2. Providers with fuzzy-matched model names
  3. Remaining providers with random model selection

`ClientCompletions.last_provider` and `ClientImages.last_provider` keep track of which provider ultimately served the request.

## ⚙️ Initialization Parameters

```python
Client(
    provider=None,                 # Default chat provider class
    image_provider=None,           # Default TTI provider class
    api_key=None,                  # Shared auth for providers that accept 'api_key'
    proxies=None,                  # Dict passed to provider constructors
    exclude=None,                  # List[str] of provider names to exclude (chat)
    exclude_images=None,           # List[str] of provider names to exclude (TTI)
    print_provider_info=False,     # Print resolved provider/model to stdout with ANSI colors
    **kwargs                       # Additional arguments passed to provider constructors
)
```

- `exclude` accepts provider names (case-insensitive) to blacklist chat providers that are unstable or premium.
- `exclude_images` accepts provider names (case-insensitive) to blacklist TTI providers.
- `print_provider_info=True` prints ANSI-colored `Provider:Model` lines whenever a provider succeeds (including fallback attempts).

## 🧩 Streaming vs Non-Streaming

When `stream=True`:
- The first chunk is fetched eagerly so the client can announce the provider and handle errors early.
- The generator yields `ChatCompletionChunk` objects exactly like the OpenAI SDK.
- If the resolved provider fails to stream, the client automatically tries other providers from the fallback queue.
- The first yielded chunk marks successful provider connection and model resolution.

When `stream=False`:
- The client inspects `response.choices[0].message.content` and validates that it's not empty/whitespace.
- If the response is empty or contains only whitespace, the client retries with other providers.
- The client returns a complete `ChatCompletion` object.

## 🖼️ Image Generation

- Uses the same resolution logic as chat completions but targets classes derived from `TTICompatibleProvider`.
- Accepts `prompt`, `model`, `n`, `size`, `response_format` (`url` or `b64_json`), plus provider-specific kwargs.
- Authentication is not required for TTI providers by default (auth providers are filtered out).
- Failover follows the same three-tiered approach (exact model → fuzzy matches → random fallback).
- Default parameters: `n=1`, `size="1024x1024"`, `response_format="url"`

## 🔐 Authentication Handling

- **Chat providers**: Only providers with `required_auth=False` are used unless `api_key` is provided.
- **TTI providers**: Only providers with `required_auth=False` are used (no auth currently supported for TTI).
- **Dynamic filtering**: Providers that declare `required_auth=True` are automatically excluded based on client configuration.
- **Instance caching**: The same provider instance is reused for multiple requests when possible to optimize performance.

## 🧾 Provider Introspection Helpers

```python
Client.get_chat_providers()        # All detected OpenAI-compatible provider names
Client.get_free_chat_providers()   # Chat providers that don't require authentication
Client.get_image_providers()       # All TTI provider names
Client.get_free_image_providers()  # TTI providers that don't require authentication
```

These introspection helpers pull data from the global `OPENAI_PROVIDERS` and `TTI_PROVIDERS` maps constructed during import time using dynamic package inspection.

## 🧪 Debugging Tips

- Set `print_provider_info=True` to see the provider/model resolution and fallback path in real time with ANSI coloring.
- Inspect `client.chat.completions.last_provider` and `client.images.last_provider` after a call to confirm where the response came from.
- Check excluded providers by examining `client.exclude` and `client.exclude_images` to ensure desired providers aren't filtered out.
- To test failover handling, deliberately exclude successful providers (`exclude=["ChatGPT"]`) and verify that other providers handle the request.

## 🧱 Internal Structure

- `load_openai_providers()` / `load_tti_providers()` use `pkgutil.iter_modules()` to dynamically discover provider classes in respective packages.
- `_get_models_safely()` safely instantiates providers (using cache when available) and calls their `models.list()` method to retrieve available models.
- Provider cache (`_provider_cache`) stores initialized provider instances to avoid repeated instantiation overhead.
- Fuzzy matching prioritizes exact matches, then substring matches, then `difflib` suggestions with 0.5 confidence threshold.
- Error handling collects provider-specific errors and raises a consolidated exception: `RuntimeError("All chat providers failed. Errors: ...")`.
- Both chat and image generation follow the same resolution and failover patterns with provider-specific implementations.

## 🔗 Related Docs

- [docs/models.md](models.md) – learn how the model registry enumerates provider/model pairs.
- [docs/openai-api-server.md](openai-api-server.md) – the FastAPI server serves models in OpenAI-compatible API format, which can be used where OpenAI API can be used; the client provides local Python access to the same providers.
- [docs/architecture.md](architecture.md) – see where the client fits relative to CLI and server layers.
- [docs/providers/](providers/) – detailed documentation for individual provider implementations.
