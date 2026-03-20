# Private_GPT Architecture Overview
> Last updated: 2025-12-20  
> Relates to: `private_gpt/cli.py`, `private_gpt/client.py`, `private_gpt/server/`, `private_gpt/search/`, `private_gpt/Provider/`, `private_gpt/Extra/`

Private_GPT bundles multiple user-facing entry points (CLI, Python client, and an OpenAI-compatible API server) on top of a shared set of engines, providers, and utilities. This document maps how these layers interact so you can reason about changes confidently.

## 🧱 Layered View

```mermaid
flowchart TD
    subgraph EntryPoints
        CLI[CLI (private_gpt/cli.py)]
        Client[Python Client (private_gpt/client.py)]
        Server[OpenAI-Compatible Server (private_gpt/server)]
    end

    subgraph Core
        Search[Search Engines (private_gpt/search)]
        Providers[Providers (private_gpt/Provider)]
        Extras[Extras & Toolkits (private_gpt/Extra)]
        Utilities[Utilities (sanitize.py, AIutel.py, etc.)]
        Models[Model Registry (private_gpt/models.py)]
    end

    CLI --> Search
    CLI --> Providers
    Client --> Providers
    Client --> Extras
    Client --> Models
    Server --> Providers
    Server --> Utilities
    Search --> Providers
    Extras --> Providers
```

- **Entry Points** convert user intent (commands/API calls) into provider requests.
- **Core Modules** encapsulate the heavy lifting: crawling websites, calling remote LLMs, handling audio/image generation, sanitizing streams, and enumerating models.

## 🔌 Entry Points

### Command Line Interface (`private_gpt/cli.py`)
- Built on `swiftcli` with separate command groups for DuckDuckGo, Yep, Bing, Yahoo, and weather utilities.
- Uses `_print_data` / `_print_weather` helpers to keep terminal output consistent.
- Relies on the same search/provider classes exported in `private_gpt/__init__.py`, so CLI behavior matches the Python API.

### Unified Python Client (`private_gpt/client.py`)
- Provides auto-failover chat and image APIs through `Client.chat.completions.create()` and `Client.images.generate()`.
- Dynamically discovers OpenAI-compatible providers (`private_gpt/Provider/OPENAI`) and TTI providers, caches instances, and performs fuzzy model resolution.
- Shares provider cache with the server, so runtime cost of imports stays low.

### OpenAI-Compatible Server (`private_gpt/server/`)
- FastAPI app that exposes `/v1/*` routes mirroring OpenAI's schema.
- Uses `providers.py` to map model names like `ProviderName/model-id` back to actual provider classes.
- Pulls configuration from `config.py` plus environment variables documented in `docs/openai-api-server.md` and `docs/DOCKER.md`.

## 🔍 Core Modules

### Search Stack (`private_gpt/search/`)
- Houses protocol-specific engines (See `private_gpt/search/engines/*`) plus shared HTTP client and result serializers.
- DuckDuckGo/Yep/Bing/Yahoo commands import from here, so adding new CLI options usually starts with an engine update.

### Providers (`private_gpt/Provider/`)
- Normal providers live alongside OpenAI-compatible wrappers (`private_gpt/Provider/OPENAI`).
- Specialty directories: `AISEARCH`, `TTI`, `TTS`, `STT`, `UNFINISHED`.
- The matrix in `Provider.md` maps every provider to its implementation file.

### Extras (`private_gpt/Extra/`)
- Optional toolkits packaged with Private_GPT (GGUF converter, weather clients, temp mail, YT toolkit, Git API helper, etc.).
- Exported through `private_gpt/Extra/__init__.py` so they become part of the public API when you `import private_gpt`.

### Utilities
- `private_gpt/sanitize.py` – SSE/stream sanitization for server + client streaming paths.
- `private_gpt/AIutel.py` – Decorators for retry/timing (documented in `docs/decorators.md`).
- `private_gpt/update_checker.py` – Optional PyPI update notifier executed in `private_gpt/__init__.py`.

### Models Registry (`private_gpt/models.py`)
- Enumerates LLM, TTS, and TTI models exposed by providers.
- Used by documentation examples (README, docs/models.md) and can power custom tooling (e.g., provider dashboards).

## 🔄 Typical Data Flows

1. **CLI ➜ Search Engine ➜ Provider**
   - `private_gpt images -k "python"` → `DuckDuckGoSearch.images()` (HTTP scraping) → results printed via `_print_data`.
2. **Client ➜ Provider Failover**
   - `Client().chat.completions.create(model="gpt-4o")` → resolves provider & model → tries preferred provider → falls back through fuzzily-matched providers if necessary.
3. **Server ➜ Provider ➜ sanitize_stream**
   - `/v1/chat/completions` request hits FastAPI → provider resolved → streaming responses run through `sanitize_stream()` before being sent to clients.
4. **Extras ➜ Providers**
   - GGUF converter uses huggingface + llama.cpp builders and is fully independent, but still exported to users alongside the main modules.

## 🧩 When Adding New Functionality

| Task | Touch Points |
|------|--------------|
| Add a CLI command | `private_gpt/cli.py` + corresponding engine/provider + update `docs/cli.md` |
| Add a provider | Implement in `private_gpt/Provider/` (and optionally `OPENAI/`), update `Provider.md`, consider `models.py` exposure |
| Add server capability | Update `private_gpt/server/*`, document in `docs/openai-api-server.md`, ensure CLI/Client can hit the new route if needed |
| Extend Extras | Implement under `private_gpt/Extra/`, export in `__init__.py`, add documentation entry under `docs/README.md` |
| Add new registry info | Update `private_gpt/models.py` or referencing docs (`docs/models.md`) |

## 🧪 Testing & Debugging Hooks

- CLI commands can be run locally with `uv run private_gpt ...` to ensure option parsing remains correct.
- Client failover prints last provider when `print_provider_info=True` – useful when debugging provider availability.
- The server exposes `/health` (see Docker docs) to monitor deployments.
- `sanitize_stream` and decorators have dedicated docs you can reference when debugging streaming issues or retries.

## 📚 Related Documents

- [docs/cli.md](cli.md) – exhaustive CLI reference.
- [docs/client.md](client.md) – deep dive into the unified client.
- [docs/models.md](models.md) – using the model registry helpers.
- [docs/openai-api-server.md](openai-api-server.md) – server configuration & endpoints.
- [Provider.md](../Provider.md) – provider matrix you can cross-reference while navigating the codebase.
