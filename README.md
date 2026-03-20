# Private_GPT
A powerful, OpenAI-compatible API server spanning across various LLMs, Search Engines, and utilities.

## Overview
Private_GPT acts as a universal router that interfaces with different AI Providers and Search Engines underneath a fully unified API surface. It allows you to seamlessly integrate various language models into applications expecting an OpenAI-compatible endpoint.

## Features
- **OpenAI-Compatible API Interface**: Drop-in replacement for OpenAI SDKs.
- **Vast Provider Support**: Native integration with multiple LLM and search base APIs.
- **Streaming Support**: True token-by-token streaming capabilities.
- **Cross-Platform**: Deployable anywhere via Docker or Render standard build environments.

## Quick Start (Deploying on Render)
This project is already pre-configured for deployment on [Render](https://render.com).

1. Go to your Render Dashboard.
2. Select **New -> Blueprint**.
3. Select your repository.
4. Render will use `render.yaml` to automatically handle all installations and spin up the FastAPI service natively.

## Manual Installation
To install and run Private_GPT manually on your local machine:

```bash
# Clone the repository
git clone <your-github-repo-url>
cd PrivateGPT

# Setup a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package with API dependencies
pip install -e ".[api]"

# Start the server
uvicorn private_gpt.server.server:app --host 0.0.0.0 --port 8000
```

## Using the API
Configure any standard OpenAI REST client to point to your new base URL:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1", # Or your Render deployment URL
    api_key="anything" # API key is ignored but required by the client
)

response = client.chat.completions.create(
    model="AI4Chat/claude-opus-4.6", # Pick a model returned by /v1/models
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

