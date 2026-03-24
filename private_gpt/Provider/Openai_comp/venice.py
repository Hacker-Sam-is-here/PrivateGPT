import json
import os
import time
import uuid
from typing import Any, Dict, Generator, Iterator, List, Optional, Union

from curl_cffi.requests import Session

from private_gpt.Extra.proxy_manager import ProxyManager
from private_gpt.Provider.Openai_comp.base import (
    BaseChat,
    BaseCompletions,
    OpenAICompatibleProvider,
    SimpleModelList,
    Tool,
)
from private_gpt.Provider.Openai_comp.utils import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    Choice,
    ChoiceDelta,
)

VENICE_HEADERS = {
    "accept": "text/event-stream",
    "accept-language": "en-GB,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://venice.ai",
    "referer": "https://venice.ai/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-venice-locale": "en",
    "x-venice-middleface-version": "0.1.555",
    "x-venice-version": "interface@20260324.041013+db0e9ee",
}

# Proxy manager with auto_fetch to bypass rate limits
pm = ProxyManager(auto_fetch=True)

class VeniceCompletions(BaseCompletions):
    def create(
        self,
        *,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Generator[ChatCompletionChunk, None, None]]:
        api_key = kwargs.get("api_key")

        # If the user passed venice_cookies.json as api_key, load it.
        # Otherwise, if they passed raw json or cookie string, use that.
        if api_key and api_key.endswith(".json") and os.path.exists(api_key):
            cookie_path = api_key
        else:
            cookie_path = "venice_cookies.json"

        if api_key and not api_key.endswith(".json"):
            try:
                # Try to parse as raw JSON dump
                cookie_list = json.loads(api_key)
            except Exception:
                # Or just treat as raw cookie string
                cookie_list = None
                cookie_str = api_key
        else:
            if not os.path.exists(cookie_path):
                raise Exception(f"{cookie_path} not found")

            with open(cookie_path) as f:
                cookie_list = json.load(f)

        if cookie_list:
            cookies = {c["name"]: c["value"] for c in cookie_list if c.get("value")}
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

        sess_headers = VENICE_HEADERS.copy()
        sess_headers["cookie"] = cookie_str
        sess_headers["x-venice-request-timestamp-ms"] = str(int(time.time() * 1000))
        sess_headers["x-venice-distinct-id"] = str(uuid.uuid4())

        payload = {
            "clientProcessingTime": 2,
            "conversationType": "text",
            "includeVeniceSystemPrompt": True,
            "isCharacter": False,
            "modelId": model,
            "prompt": messages,
            "reasoning": False,
            "requestId": uuid.uuid4().hex[:7],
            "simpleMode": False,
            "systemPrompt": "",
            "temperature": kwargs.get("temperature", 0.7),
            "topP": kwargs.get("top_p", 0.9),
            "userId": "user_anon_1234568910",
            "webEnabled": True,
            "webScrapeEnabled": False,
            "xSearchEnabled": False
        }

        def _generator():
            max_retries = 20
            last_err = None
            for attempt in range(max_retries):
                proxies = pm.get() # Get proxy dict for this rotation

                try:
                    with Session(
                        impersonate="chrome",
                        headers=sess_headers,
                        proxies=proxies,
                        timeout=timeout or 300
                    ) as session:
                        resp = session.post(
                            "https://outerface.venice.ai/api/inference/chat",
                            json=payload,
                            stream=True
                        )

                        # Check if successful response
                        if resp.status_code != 200:
                            if attempt < max_retries - 1:
                                continue
                            raise Exception(f"Venice error: HTTP {resp.status_code} - {resp.text}")

                        for line in resp.iter_lines():
                            if not line:
                                continue
                            line_str = line.decode("utf-8").strip()

                            if line_str.startswith("data: "):
                                line_str = line_str[6:].strip()

                            if line_str == "[DONE]":
                                return # Clean exit

                            try:
                                data = json.loads(line_str)
                                content = ""

                                if "content" in data:
                                    content = data["content"]
                                elif "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        content = delta["content"]
                                    elif "text" in data["choices"][0]:
                                        content = data["choices"][0]["text"]

                                if content:
                                    chunk = ChatCompletionChunk(
                                        id=f"chatcmpl-{uuid.uuid4()}",
                                        choices=[
                                            Choice(
                                                index=0,
                                                delta=ChoiceDelta(content=content, role="assistant"),
                                                logprobs=None,
                                                finish_reason=None
                                            )
                                        ],
                                        created=int(time.time()),
                                        model=model,
                                        object="chat.completion.chunk"
                                    )
                                    yield chunk
                            except json.JSONDecodeError:
                                continue
                        return # Finished successfully

                except Exception as e:
                    last_err = e
                    continue # Retry on error

            if last_err:
                raise last_err
        if stream:
            return _generator()
        else:
            full_response = ""
            for chunk in _generator():
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content

            return ChatCompletion(
                id=f"chatcmpl-{uuid.uuid4()}",
                choices=[
                    Choice(
                        index=0,
                        message=ChatCompletionMessage(role="assistant", content=full_response),
                        finish_reason="stop",
                        logprobs=None,
                        delta=ChoiceDelta()
                    )
                ],
                created=int(time.time()),
                model=model,
                object="chat.completion"
            )

class VeniceChat(BaseChat):
    def __init__(self, provider: OpenAICompatibleProvider):
        self.completions = VeniceCompletions()

class Venice(OpenAICompatibleProvider):
    required_auth = True
    AVAILABLE_MODELS = [
        "dolphin-3.0-mistral-24b-1dot1"
    ]

    @property
    def models(self) -> SimpleModelList:
        return SimpleModelList(self.AVAILABLE_MODELS)

    @property
    def chat(self) -> VeniceChat:
        return VeniceChat(self)
