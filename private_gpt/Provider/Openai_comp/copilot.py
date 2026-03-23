import os
import json
import uuid
import time
import asyncio
import threading
import queue
from typing import Any, Dict, Generator, List, Optional, Union, cast

from curl_cffi.requests import AsyncSession
from curl_cffi import CurlWsFlag

from private_gpt.Provider.Openai_comp.base import (
    BaseChat,
    BaseCompletions,
    OpenAICompatibleProvider,
    SimpleModelList,
)
from private_gpt.Provider.Openai_comp.utils import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    Choice,
    ChoiceDelta,
    CompletionUsage,
    format_prompt,
)

HEADERS = {
    "origin": "https://copilot.microsoft.com",
    "referer": "https://copilot.microsoft.com/",
}

class Completions(BaseCompletions):
    def __init__(self, client: "Copilot"):
        self._client = client

    def create(
        self,
        *,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        stream: bool = False,
        timeout: Optional[int] = None,
        proxies: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Generator[ChatCompletionChunk, None, None]]:
        mapped_model = "smart"
        if "reasoning" in model.lower() or "deep" in model.lower() or "think" in model.lower():
            mapped_model = "reasoning"
        elif "chat" in model.lower():
            mapped_model = "chat"
            
        cookies = self._client.load_cookies()
        if not cookies:
            raise ValueError(f"Could not load cookies from: {self._client.api_key}")
            
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items() if v])
        sess_headers = HEADERS.copy()
        sess_headers["cookie"] = cookie_str
        
        prompt = format_prompt(messages)
        
        def generate() -> Generator[ChatCompletionChunk, None, None]:
            chat_id = f"chatcmpl-{uuid.uuid4()}"
            created_time = int(time.time())
            
            q = queue.Queue()
            
            async def run_async():
                try:
                    async with AsyncSession(
                        impersonate="chrome", 
                        headers=sess_headers, 
                        timeout=30, 
                        proxies=proxies or self._client.proxies
                    ) as session:
                        start_payload = {
                            "timeZone": "America/Los_Angeles",
                            "startNewConversation": True,
                            "teenSupportEnabled": True,
                            "correctPersonalizationSetting": True,
                            "performUserMerge": True,
                            "deferredDataUseCapable": True
                        }
                        
                        resp = await session.post(
                            "https://copilot.microsoft.com/c/api/start",
                            json=start_payload,
                            headers={"content-type": "application/json"}
                        )
                        if resp.status_code != 200:
                            q.put(("error", RuntimeError(f"Copilot API start failed [{resp.status_code}]: {resp.text}")))
                            return
                            
                        start_data = resp.json()
                        conv_id = start_data["currentConversationId"]
                        session.cookies.update(resp.cookies)
                        
                        ws_url = f"wss://copilot.microsoft.com/c/api/chat?api-version=2&clientSessionId={uuid.uuid4()}"
                        wss = await session.ws_connect(ws_url, timeout=15)
                        
                        msg_payload = {
                            "event": "send",
                            "conversationId": conv_id,
                            "content": [{
                                "type": "text",
                                "text": prompt,
                            }],
                            "mode": mapped_model,
                        }
                        
                        await wss.send(json.dumps(msg_payload).encode(), CurlWsFlag.TEXT)
                        
                        done = False
                        while not wss.closed and not done:
                            try:
                                msg_txt, _ = await wss.recv()
                            except Exception as e:
                                break
                                
                            try:
                                msg = json.loads(msg_txt)
                            except json.JSONDecodeError:
                                continue
                                
                            event = msg.get("event")
                            if event == "appendText" and "text" in msg:
                                q.put(("item", msg["text"]))
                            elif event == "done":
                                done = True
                            elif event == "error":
                                error_msg = f"\n[Error: {msg.get('message', msg)}]"
                                q.put(("item", error_msg))
                                done = True
                                
                        if not wss.closed:
                            await wss.close()
                except Exception as e:
                    q.put(("error", e))
                finally:
                    q.put(("done", None))

            def target():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(run_async())
                loop.close()

            t = threading.Thread(target=target)
            t.start()
            
            while True:
                kind, val = q.get()
                if kind == "done":
                    break
                elif kind == "error":
                    yield ChatCompletionChunk(
                        id=chat_id,
                        created=created_time,
                        model=mapped_model,
                        choices=[
                            Choice(
                                index=0,
                                delta=ChoiceDelta(content=f"\n[Provider Error]: {str(val)}", role="assistant"),
                            )
                        ],
                    )
                    break
                else:
                    yield ChatCompletionChunk(
                        id=chat_id,
                        created=created_time,
                        model=mapped_model,
                        choices=[
                            Choice(
                                index=0,
                                delta=ChoiceDelta(content=val, role="assistant"),
                            )
                        ],
                    )
            t.join()

        if stream:
            return generate()
        else:
            full_text = ""
            for chunk in generate():
                if chunk.choices and chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
            
            return ChatCompletion(
                id=f"chatcmpl-{uuid.uuid4()}",
                created=int(time.time()),
                model=mapped_model,
                choices=[
                    Choice(
                        index=0,
                        message=ChatCompletionMessage(content=full_text, role="assistant"),
                        finish_reason="stop",
                    )
                ],
                usage=CompletionUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )

class Chat(BaseChat):
    def __init__(self, client: "Copilot"):
        self._client = client

    @property
    def completions(self) -> Completions:
        return Completions(self._client)

class Copilot(OpenAICompatibleProvider):
    # This class integrates Microsoft Copilot into the OpenAI framework
    required_auth = True
    AVAILABLE_MODELS = ["smart", "reasoning", "chat"]
    
    def __init__(self, api_key: Optional[str] = None, proxies: Optional[Dict[str, str]] = None, **kwargs: Any):
        super().__init__(api_key=api_key, proxies=proxies, **kwargs)
        self.api_key = api_key or "copilot_cookies.json"
        
    @property
    def models(self) -> SimpleModelList:
        return SimpleModelList(["smart", "reasoning", "chat"])

    @property
    def chat(self) -> Chat:
        return Chat(self)

    def load_cookies(self) -> dict:
        if not os.path.exists(self.api_key):
            return {}
        try:
            with open(self.api_key) as f:
                cookie_list = json.load(f)
            return {c["name"]: c["value"] for c in cookie_list if c.get("value")}
        except Exception:
            return {}
