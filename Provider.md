# Private_GPT Provider Documentation

This document provides a comprehensive overview of all AI providers available in the Private_GPT library, categorized by their implementation types.


## Table of Contents
- [Overview](#overview)
- [Providers with Both Normal and OpenAI-Compatible Versions](#providers-with-both-normal-and-openai-compatible-versions)
- [Providers with Only Normal Version](#providers-with-only-normal-version)
- [Providers with Only OpenAI-Compatible Version](#providers-with-only-openai-compatible-version)
- [Statistics](#statistics)
- [Provider Categories](#provider-categories)

## Overview

Private_GPT supports multiple AI providers with different implementation approaches:
- **Normal Providers**: Standard implementation located in `private_gpt/Provider/`
- **OpenAI-Compatible Providers**: OpenAI API-compatible implementation located in `private_gpt/Provider/Openai_comp/`
- **Hybrid Providers**: Available in both normal and OpenAI-compatible versions

---

## Providers with Both Normal and OpenAI-Compatible Versions

These providers have both standard and OpenAI-compatible implementations, giving users flexibility in how they interact with the API.

| # | Provider Name | Normal Path | OpenAI Path |
|---|---------------|-------------|-------------|
| 1 | **AI4Chat** | `private_gpt/Provider/ai4chat.py` | `private_gpt/Provider/Openai_comp/ai4chat.py` |
| 2 | **AkashGPT** | `private_gpt/Provider/akashgpt.py` | `private_gpt/Provider/Openai_comp/akashgpt.py` |
| 3 | **Algion** | `private_gpt/Provider/Algion.py` | `private_gpt/Provider/Openai_comp/algion.py` |
| 4 | **Cerebras** | `private_gpt/Provider/cerebras.py` | `private_gpt/Provider/Openai_comp/cerebras.py` |
| 5 | **DeepAI** | `private_gpt/Provider/DeepAI.py` | `private_gpt/Provider/Openai_comp/DeepAI.py` |
| 6 | **DeepInfra** | `private_gpt/Provider/Deepinfra.py` | `private_gpt/Provider/Openai_comp/deepinfra.py` |
| 7 | **Elmo** | `private_gpt/Provider/elmo.py` | `private_gpt/Provider/Openai_comp/elmo.py` |
| 8 | **ExaAI** | `private_gpt/Provider/ExaAI.py` | `private_gpt/Provider/Openai_comp/exaai.py` |
| 9 | **Ayle** | `private_gpt/Provider/Ayle.py` | `private_gpt/Provider/Openai_comp/ayle.py` |
| 10 | **Groq** | `private_gpt/Provider/Groq.py` | `private_gpt/Provider/Openai_comp/groq.py` |
| 11 | **HeckAI** | `private_gpt/Provider/HeckAI.py` | `private_gpt/Provider/Openai_comp/heckai.py` |
| 12 | **HuggingFace** | `private_gpt/Provider/HuggingFace.py` | `private_gpt/Provider/Openai_comp/huggingface.py` |
| 13 | **IBM** | `private_gpt/Provider/IBM.py` | `private_gpt/Provider/Openai_comp/ibm.py` |
| 14 | **K2Think** | `private_gpt/Provider/k2think.py` | `private_gpt/Provider/Openai_comp/k2think.py` |
| 15 | **LLMChatCo** | `private_gpt/Provider/llmchatco.py` | `private_gpt/Provider/Openai_comp/llmchatco.py` |
| 17 | **Netwrck** | `private_gpt/Provider/Netwrck.py` | `private_gpt/Provider/Openai_comp/netwrck.py` |
| 18 | **Nvidia** | `private_gpt/Provider/Nvidia.py` | `private_gpt/Provider/Openai_comp/nvidia.py` |
| 19 | **OIVSCode** | `private_gpt/Provider/oivscode.py` | `private_gpt/Provider/Openai_comp/oivscode.py` |
| 20 | **PI** | `private_gpt/Provider/PI.py` | `private_gpt/Provider/Openai_comp/PI.py` |
| 21 | **Sonus** | `private_gpt/Provider/sonus.py` | `private_gpt/Provider/Openai_comp/sonus.py` |
| 22 | **TextPollinationsAI** | `private_gpt/Provider/TextPollinationsAI.py` | `private_gpt/Provider/Openai_comp/textpollinations.py` |
| 23 | **TogetherAI** | `private_gpt/Provider/TogetherAI.py` | `private_gpt/Provider/Openai_comp/TogetherAI.py` |
| 24 | **Toolbaz** | `private_gpt/Provider/toolbaz.py` | `private_gpt/Provider/Openai_comp/toolbaz.py` |
| 25 | **TwoAI** | `private_gpt/Provider/TwoAI.py" | `private_gpt/Provider/Openai_comp/TwoAI.py` |
| 26 | **WiseCat** | `private_gpt/Provider/WiseCat.py` | `private_gpt/Provider/Openai_comp/wisecat.py` |
| 29 | **X0GPT** | `private_gpt/Provider/x0gpt.py` | `private_gpt/Provider/Openai_comp/x0gpt.py` |
| 30 | **Yep** | `private_gpt/Provider/yep.py` | `private_gpt/Provider/Openai_comp/yep.py` |

| 32 | **Sambanova** | `private_gpt/Provider/Sambanova.py` | `private_gpt/Provider/Openai_comp/sambanova.py` |
| 33 | **Meta** | `private_gpt/Provider/meta.py` | `private_gpt/Provider/Openai_comp/meta.py` |
| 34 | **TypliAI** | `private_gpt/Provider/TypliAI.py` | `private_gpt/Provider/Openai_comp/typliai.py` |
| 35 | **LLMChat** | `private_gpt/Provider/llmchat.py` | `private_gpt/Provider/Openai_comp/llmchat.py` |

| 37 | **OpenRouter** | `private_gpt/Provider/OpenRouter.py` | `private_gpt/Provider/Openai_comp/openrouter.py` |

**Total: 37 providers with dual implementations**

---

## Providers with Only Normal Version

These providers are only available in the standard implementation format.

| # | Provider Name | Path |
|---|---------------|------|
| 1 | **Apriel** | `private_gpt/Provider/Apriel.py` |
| 2 | **Cohere** | `private_gpt/Provider/Cohere.py` |
| 5 | **EssentialAI** | `private_gpt/Provider/EssentialAI.py` |
| 6 | **Falcon** | `private_gpt/Provider/Falcon.py` |
| 7 | **Gemini** | `private_gpt/Provider/Gemini.py` |
| 8 | **GeminiAPI** | `private_gpt/Provider/geminiapi.py` |
| 9 | **GithubChat** | `private_gpt/Provider/GithubChat.py` |
| 10 | **Jadve** | `private_gpt/Provider/Jadve.py` |
| 11 | **Julius** | `private_gpt/Provider/julius.py` |

| 13 | **OpenAI** | `private_gpt/Provider/Openai.py` |
| 16 | **QwenLM** | `private_gpt/Provider/QwenLM.py` |
| 17 | **SearchChat** | `private_gpt/Provider/searchchat.py` |
| 18 | **TurboSeek** | `private_gpt/Provider/turboseek.py` |
| 19 | **Upstage** | `private_gpt/Provider/Upstage.py` |
| 20 | **WrDoChat** | `private_gpt/Provider/WrDoChat.py` |

**Total: 17 providers with only normal implementation**

---

## Providers with Only OpenAI-Compatible Version

These providers are only available in the OpenAI-compatible format and have no standard implementation.

| # | Provider Name | Path |
|---|---------------|------|
| 1 | **ChatGPT** | `private_gpt/Provider/Openai_comp/chatgpt.py` |
| 2 | **E2B** | `private_gpt/Provider/Openai_comp/e2b.py` |
| 3 | **FreeAssist** | `private_gpt/Provider/Openai_comp/freeassist.py` |
| 4 | **WriteCream** | `private_gpt/Provider/Openai_comp/writecream.py` |
| 5 | **Zenmux** | `private_gpt/Provider/Openai_comp/zenmux.py` |

**Total: 5 providers with only OpenAI-compatible implementation**

---

## Statistics

### Provider Distribution

```
┌─────────────────────────────────────────┬───────┐
│ Category                                │ Count │
├─────────────────────────────────────────┼───────┤
│ Both Normal & OpenAI-Compatible         │  37   │
│ Only Normal Version                     │  21   │
│ Only OpenAI-Compatible Version          │   5   │
├─────────────────────────────────────────┼───────┤
│ TOTAL UNIQUE PROVIDERS                  │  63   │
└─────────────────────────────────────────┴───────┘
```

### Implementation Coverage

- **Total Normal Implementations**: 58 (37 hybrid + 21 normal-only)
- **Total OpenAI Implementations**: 42 (37 hybrid + 5 OpenAI-only)
- **Providers with Multiple Options**: 37 (59% of all providers)

---


### Text-to-Image Providers
Located in `private_gpt/Provider/TTI/`:
- AI Arta
- Bing
- Claude Online
- GPT1 Image
- Imagen
- Infip
- Magic Studio
- MonoChat
- PicLumen
- PixelMuse
- Pollinations
- Together

### Text-to-Speech Providers
Located in `private_gpt/Provider/TTS/`:
- DeepGram
- ElevenLabs
- FreeTTS
- Gesserit
- Murf AI
- OpenAI FM
- Parler
- SpeechMA
- Stream Elements

### Speech-to-Text Providers
Located in `private_gpt/Provider/STT/`:
- ElevenLabs

### Unfinished/Experimental Providers
Located in `private_gpt/Provider/UNFINISHED/`:
- ChatHub
- ChutesAI
- GizAI
- Liner
- Marcus
- Qodo
- Samurai
- XenAI
- YouChat

---
## Usage Notes

### Choosing Between Normal and OpenAI-Compatible Versions

**Use Normal Version when:**
- You want provider-specific features and customizations
- You need direct access to native provider capabilities
- You're building custom integrations

**Use OpenAI-Compatible Version when:**
- You want to easily switch between providers without code changes
- You're migrating from OpenAI and want minimal code changes
- You need standardized API interface across multiple providers

### Normal Provider Implementation
Concrete guidance when creating a "normal" (non-OpenAI-compatible) provider under `private_gpt/Provider/`:
- Subclass `Provider` from `private_gpt.AIbase` and implement these methods: `ask(prompt, ...)`, `chat(prompt, ...)`, and `get_message(response)`.
- Keep provider class names and filenames consistent (CamelCase class name matching the filename) and add a static import in `private_gpt/Provider/__init__.py` to expose the provider at the package root.
- Prefer `requests.Session` for HTTP clients and avoid global mutable state so provider instances are safe to reuse.
- Add unit tests under `tests/providers/` that mock HTTP and validate normal and error behavior (including streaming if supported).
- Document the provider in `Provider.md` and a short usage snippet in `docs/` when appropriate.

### Use uv for All Commands
We use `uv` to manage the Python environment and run tools. Never run bare `python` or `pip` directly — always run commands with `uv` to avoid environment drift and to use the project's lockfile. Examples:
- `uv add <package>` / `uv remove <package>` — manage dependencies
- `uv sync` — install dependencies declared in `pyproject.toml` and `uv.lock`
- `uv run <command>` — run a script or tool inside the uv environment (e.g., `uv run pytest`, `uv run private_gpt`)
- `uv run --extra api private_gpt-server` — run the API server with extra dependencies

### Example Usage

```python
# Normal Provider
from private_gpt.Provider import Groq
provider = Groq()
response = provider.chat("Hello, how are you?")

# OpenAI-Compatible Provider
from private_gpt.Provider.Openai_comp import groq
client = groq.GroqProvider()
response = client.chat.completions.create(
    model="mixtral-8x7b",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
```

---

## Contributing

When adding new providers:
1. Implement the normal version in `private_gpt/Provider/`
2. If applicable, create an OpenAI-compatible version in `private_gpt/Provider/Openai_comp/`
3. Update this documentation
4. Add tests for both implementations

---

## License

This documentation is part of the Private_GPT project. See LICENSE.md for details.

---

**Last Updated**: 2025
**Version**: 1.0
**Maintained by**: Private_GPT Development Team