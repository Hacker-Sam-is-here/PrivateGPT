import json
import random
import re
import time
import uuid
from typing import Any, Callable, Dict, Generator, List, Optional, Union, cast

from curl_cffi.requests import RequestsError, Session

from private_gpt.AIbase import Response
from private_gpt.litagent import LitAgent

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
    count_tokens,
    get_last_user_message,
)

# ==================== Qwen Anti-Bot Config ====================
CUSTOM_BASE64_CHARS = "DGi0YA7BemWnQjCl4_bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ"
HASH_FIELDS = {16: "split", 17: "full", 18: "full", 31: "full", 34: "full", 36: "full"}

def lzw_compress(data: Optional[str], bits: int, char_func: Callable[[int], str]) -> str:
    if data is None: return ""
    dictionary, dict_to_create = {}, {}
    w, enlarge_in, dict_size, num_bits = "", 2, 3, 2
    result, value, position = [], 0, 0
    for i in range(len(data)):
        c = data[i]
        if c not in dictionary:
            dictionary[c] = dict_size
            dict_size += 1
            dict_to_create[c] = True
        wc = w + c
        if wc in dictionary: w = wc
        else:
            if w in dict_to_create:
                if ord(w[0]) < 256:
                    for _ in range(num_bits):
                        value = (value << 1)
                        if position == bits - 1:
                            position, result, value = 0, result + [char_func(value)], 0
                        else: position += 1
                    char_code = ord(w[0])
                    for _ in range(8):
                        value = (value << 1) | (char_code & 1)
                        if position == bits - 1:
                            position, result, value = 0, result + [char_func(value)], 0
                        else: position += 1
                        char_code >>= 1
                else:
                    char_code = 1
                    for _ in range(num_bits):
                        value = (value << 1) | char_code
                        if position == bits - 1:
                            position, result, value = 0, result + [char_func(value)], 0
                        else: position += 1
                        char_code = 0
                    char_code = ord(w[0])
                    for _ in range(16):
                        value = (value << 1) | (char_code & 1)
                        if position == bits - 1:
                            position, result, value = 0, result + [char_func(value)], 0
                        else: position += 1
                        char_code >>= 1
                enlarge_in -= 1
                if enlarge_in == 0:
                    enlarge_in, num_bits = 2 ** num_bits, num_bits + 1
                del dict_to_create[w]
            else:
                char_code = dictionary[w]
                for _ in range(num_bits):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position, result, value = 0, result + [char_func(value)], 0
                    else: position += 1
                    char_code >>= 1
            enlarge_in -= 1
            if enlarge_in == 0: enlarge_in, num_bits = 2 ** num_bits, num_bits + 1
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w != "":
        if w in dict_to_create:
            if ord(w[0]) < 256:
                for _ in range(num_bits):
                    value = (value << 1)
                    if position == bits - 1:
                        position, result, value = 0, result + [char_func(value)], 0
                    else: position += 1
                char_code = ord(w[0])
                for _ in range(8):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position, result, value = 0, result + [char_func(value)], 0
                    else: position += 1
                    char_code >>= 1
            else:
                char_code = 1
                for _ in range(num_bits):
                    value = (value << 1) | char_code
                    if position == bits - 1:
                        position, result, value = 0, result + [char_func(value)], 0
                    else: position += 1
                    char_code = 0
                char_code = ord(w[0])
                for _ in range(16):
                    value = (value << 1) | (char_code & 1)
                    if position == bits - 1:
                        position, result, value = 0, result + [char_func(value)], 0
                    else: position += 1
                    char_code >>= 1
            enlarge_in -= 1
            if enlarge_in == 0: enlarge_in, num_bits = 2 ** num_bits, num_bits + 1
            del dict_to_create[w]
        else:
            char_code = dictionary[w]
            for _ in range(num_bits):
                value = (value << 1) | (char_code & 1)
                if position == bits - 1:
                    position, result, value = 0, result + [char_func(value)], 0
                else: position += 1
                char_code >>= 1
        enlarge_in -= 1
        if enlarge_in == 0: enlarge_in, num_bits = 2 ** num_bits, num_bits + 1
    char_code = 2
    for _ in range(num_bits):
        value = (value << 1) | (char_code & 1)
        if position == bits - 1:
            position, result, value = 0, result + [char_func(value)], 0
        else: position += 1
        char_code >>= 1
    while True:
        value = (value << 1)
        if position == bits - 1:
            result.append(char_func(value))
            break
        position += 1
    return "".join(result)

def custom_encode(data: Optional[str], url_safe: bool) -> str:
    if data is None: return ""
    compressed = lzw_compress(data, 6, lambda index: CUSTOM_BASE64_CHARS[index])
    if not url_safe:
        mod = len(compressed) % 4
        if mod == 1: return compressed + "==="
        if mod == 2: return compressed + "=="
        if mod == 3: return compressed + "="
    return compressed

def random_hash() -> int: return random.randint(0, 0xFFFFFFFF)

def generate_mock_fingerprint() -> str:
    fields = ["" for _ in range(38)]
    fields[0] = "".join(random.choice("0123456789abcdef") for _ in range(20))
    fields[1] = "1.0.0"
    fields[16] = f"0|{random_hash()}"
    fields[17] = str(random_hash())
    fields[18] = str(random_hash())
    fields[23] = "P"
    fields[31] = str(random_hash())
    fields[32] = "11"
    fields[33] = str(int(time.time() * 1000))
    fields[34] = str(random_hash())
    fields[36] = str(random.randint(10, 100))
    return "^".join(fields)

def generate_cookies() -> Dict[str, Any]:
    fields = generate_mock_fingerprint().split("^")
    processed = list(fields)
    for idx, typ in HASH_FIELDS.items():
        if idx >= len(processed): continue
        if typ == "split":
            val = str(processed[idx]).split("|")
            if len(val) == 2: processed[idx] = f"{val[0]}|{random_hash()}"
        elif typ == "full":
            processed[idx] = random.randint(10, 100) if idx == 36 else random_hash()
    if 33 < len(processed): processed[33] = int(time.time() * 1000)

    ssxmod_itna_data = "^".join(map(str, processed))
    ssxmod_itna2_data = "^".join(map(str, [
        processed[0], processed[1], processed[23], 0, "", 0, "", "", 0, 0, 0,
        processed[32], processed[33], 0, 0, 0, 0, 0
    ]))
    return {
        "ssxmod_itna": "1-" + custom_encode(ssxmod_itna_data, True),
        "ssxmod_itna2": "1-" + custom_encode(ssxmod_itna2_data, True),
    }

# --- QwenChat Client ---

class Completions(BaseCompletions):
    def __init__(self, client: "QwenChat"):
        self._client = client

    def create(
        self,
        *,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = 2049,
        stream: bool = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Union[Dict[str, Any], Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        timeout: Optional[int] = None,
        proxies: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Generator[ChatCompletionChunk, None, None]]:

        base_url = "https://chat.qwen.ai"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': base_url,
            'Referer': f'{base_url}/',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Source': 'web'
        }

        cookies_data = generate_cookies()
        headers['Cookie'] = f'ssxmod_itna={cookies_data["ssxmod_itna"]};ssxmod_itna2={cookies_data["ssxmod_itna2"]}'

        session = self._client.session
        proxy_url = proxies.get("all") if proxies else self._client.session.proxies.get("all")

        # Phase 1: Get Midtoken
        r = session.get('https://sg-wum.alibaba.com/w/wu.json', proxies={"all": proxy_url} if proxy_url else None)
        match = re.search(r"(?:umx\.wu|__fycb)\('([^']+)'\)", r.text)
        midtoken = match.group(1) if match else None
        if midtoken:
            headers['bx-umidtoken'] = midtoken
            headers['bx-v'] = '2.5.31'

        # Phase 2: Create Chat
        chat_payload = {
            "title": "New Chat",
            "models": [model],
            "chat_mode": "normal",
            "chat_type": "t2t",
            "timestamp": int(time.time() * 1000)
        }
        r2 = session.post(f'{base_url}/api/v2/chats/new', json=chat_payload, headers=headers, proxies={"all": proxy_url} if proxy_url else None)
        r2.raise_for_status()
        
        chat_data = r2.json()
        chat_id = chat_data.get('data', {}).get('id')
        if not chat_id:
            raise RequestsError(f"Failed to create chat. Response: {chat_data}")

        prompt = get_last_user_message(messages)

        msg_payload = {
            "stream": stream,
            "incremental_output": stream,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": model,
            "parent_id": None,
            "messages": [{
                "fid": str(uuid.uuid4()),
                "parentId": None,
                "childrenIds": [],
                "role": "user",
                "content": prompt, # NOTE: It only supports last user message for now in this wrapper
                "user_action": "chat",
                "files": [],
                "models": [model],
                "chat_type": "t2t",
                "feature_config": {
                    "thinking_enabled": False,
                    "output_schema": "phase",
                    "thinking_budget": 81920
                },
                "sub_chat_type": "t2t"
            }]
        }

        # Setup streaming generator
        if stream:
            response = session.post(f'{base_url}/api/v2/chat/completions?chat_id={chat_id}', json=msg_payload, headers=headers, proxies={"all": proxy_url} if proxy_url else None, stream=True)
            return self._stream_response(response, model)
        else:
            response = session.post(f'{base_url}/api/v2/chat/completions?chat_id={chat_id}', json=msg_payload, headers=headers, proxies={"all": proxy_url} if proxy_url else None)
            return self._process_response(response.json(), model)

    def _stream_response(
        self, response: Response, model: str
    ) -> Generator[ChatCompletionChunk, None, None]:
        chat_id = "chatcmpl-" + str(uuid.uuid4())
        created = int(time.time())

        for line in response.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            if not line.startswith("data:"):
                continue

            json_str = line[5:].strip()
            if json_str == "[DONE]":
                break

            try:
                data = json.loads(json_str)
                choices = data.get("choices", [])
                if not choices:
                    continue
                
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield ChatCompletionChunk(
                        id=chat_id,
                        object="chat.completion.chunk",
                        created=created,
                        model=model,
                        choices=[Choice(index=0, delta=ChoiceDelta(role="assistant", content=content))],
                    )
                
                if delta.get("status") == "finished":
                    break
            except json.JSONDecodeError:
                pass

        # Yield final DONE chunk
        yield ChatCompletionChunk(
            id=chat_id,
            object="chat.completion.chunk",
            created=created,
            model=model,
            choices=[Choice(index=0, delta=ChoiceDelta(role="assistant", content=""), finish_reason="stop")],
        )

    def _process_response(self, response_data: Dict[str, Any], model: str) -> ChatCompletion:
        chat_id = "chatcmpl-" + str(uuid.uuid4())
        created = int(time.time())
        choices = response_data.get("choices", [])
        content = ""
        
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            
        return ChatCompletion(
            id=chat_id,
            object="chat.completion",
            created=created,
            model=model,
            choices=[
                Choice(
                    index=0,
                    message=ChatCompletionMessage(role="assistant", content=content),
                    finish_reason="stop"
                )
            ],
            usage=CompletionUsage(prompt_tokens=0, completion_tokens=count_tokens(content), total_tokens=count_tokens(content)),
        )

class Chat(BaseChat):
    def __init__(self, client: "QwenChat"):
        self.completions = Completions(client)

class QwenChat(OpenAICompatibleProvider):
    name = "QwenChat"
    AVAILABLE_MODELS = [
        "qwen3.5-plus",
        "qwen3.5-flash",
        "qwen3.5-397b-a17b",
        "qwen3-max-preview",
        "qwen-plus-2025-09-11",
        "qwen3-235b-a22b",
        "qwen3-coder-plus",
        "qwen3-30b-a3b",
        "qwen3-coder-30b-a3b-instruct",
        "qwen-max-latest",
        "qwen-plus-2025-01-25",
        "qwq-32b",
        "qwen-turbo-2025-02-11",
        "qwen2.5-omni-7b",
        "qvq-72b-preview-0310",
        "qwen2.5-vl-32b-instruct",
        "qwen2.5-14b-instruct-1m",
        "qwen2.5-coder-32b-instruct",
        "qwen2.5-72b-instruct",
    ]
    required_auth = False

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        proxies: Optional[Dict[str, str]] = None,
        impersonate: Optional[str] = "chrome110",
        **kwargs: Any,
    ):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            proxies=proxies,
            impersonate=impersonate,
            **kwargs,
        )
        self.chat = Chat(self)

    @property
    def models(self) -> SimpleModelList:
        return SimpleModelList(
            [
                "qwen3-235b-a22b",
                "qwen-plus-2025-01-25",
                "qwq-32b",
                "qwen-turbo-2025-02-11",
                "qwen2.5-omni-7b",
                "qwen2.5-vl-32b-instruct",
            ]
        )
