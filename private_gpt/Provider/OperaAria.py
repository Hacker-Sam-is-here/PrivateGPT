import base64
import json
import os
import random
import time
from typing import Any, Dict, Generator, Optional, Union, cast

from curl_cffi.requests import Session
from curl_cffi.requests.exceptions import RequestException

from private_gpt import exceptions
from private_gpt.AIbase import Provider, Response
from private_gpt.AIutel import Conversation as GPtConversation

try:
    from private_gpt.Extra.proxy_manager import ProxyManager
    opera_proxy_manager = ProxyManager()
except ImportError:
    opera_proxy_manager = None


class OperaConversation:
    def __init__(self, refresh_token: str | None = None):
        self.refresh_token = refresh_token
        self.encryption_key = base64.b64encode(os.urandom(32)).decode('utf-8')
        self.is_first_request = True
        self.access_token = None
        self.expires_at = 0
        self.conversation_id = '-'.join([
            ''.join(random.choices('0123456789abcdef', k=8)),
            ''.join(random.choices('0123456789abcdef', k=4)),
            '11f0',
            ''.join(random.choices('0123456789abcdef', k=4)),
            ''.join(random.choices('0123456789abcdef', k=12))
        ])

    def is_token_expired(self) -> bool:
        return time.time() >= self.expires_at

    def update_token(self, access_token: str, expires_in: int):
        self.access_token = access_token
        self.expires_at = time.time() + expires_in - 60


class OperaAria(Provider):
    """
    A class to interact with the Opera Aria API.
    """
    required_auth = False
    AVAILABLE_MODELS = ["aria"]

    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 600,
        timeout: int = 30,
        intro: Optional[str] = None,
        filepath: Optional[str] = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: Optional[str] = None,
    ) -> None:
        self.session = Session(impersonate="chrome110")
        if proxies:
            self.session.proxies.update(proxies)
        elif opera_proxy_manager:
            pm_proxies = opera_proxy_manager.get()
            if pm_proxies:
                self.session.proxies.update(pm_proxies)

        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.timeout = timeout
        self.last_response = {}

        self.api_endpoint = "https://composer.opera-api.com/api/v1/a-chat"
        self.token_endpoint = "https://oauth2.opera-api.com/oauth2/v1/token/"
        self.signup_endpoint = "https://auth.opera.com/account/v2/external/anonymous/signup"

        self.opera_conversation = OperaConversation()
        self.conversation = GPtConversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset

        if intro:
            self.conversation.intro = intro

        elif act:
            # act handling if required, usually AIutel has AwesomePrompts
            pass

    def _generate_refresh_token(self) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": "ofa-client",
            "client_secret": "N9OscfA3KxlJASuIe29PGZ5RpWaMTBoy",
            "grant_type": "client_credentials",
            "scope": "anonymous_account"
        }
        response = self.session.post(self.token_endpoint, headers=headers, data=data, timeout=self.timeout)
        response.raise_for_status()
        anonymous_token_data = response.json()
        anonymous_access_token = anonymous_token_data["access_token"]

        headers = {
            "User-Agent": "Mozilla 5.0 (Linux; Android 14) com.opera.browser OPR/89.5.4705.84314",
            "Authorization": f"Bearer {anonymous_access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        }
        data = {"client_id": "ofa", "service": "aria"}
        response = self.session.post(self.signup_endpoint, headers=headers, json=data, timeout=self.timeout)
        response.raise_for_status()
        signup_data = response.json()
        auth_token = signup_data["token"]

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "auth_token": auth_token,
            "client_id": "ofa",
            "device_name": "GPT4FREE",
            "grant_type": "auth_token",
            "scope": "ALL"
        }
        response = self.session.post(self.token_endpoint, headers=headers, data=data, timeout=self.timeout)
        response.raise_for_status()
        final_token_data = response.json()
        return final_token_data["refresh_token"]

    def _get_access_token(self) -> str:
        if not self.opera_conversation.refresh_token:
            self.opera_conversation.refresh_token = self._generate_refresh_token()

        if self.opera_conversation.access_token and not self.opera_conversation.is_token_expired():
            return self.opera_conversation.access_token

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
        }
        data = {
            "client_id": "ofa",
            "grant_type": "refresh_token",
            "refresh_token": self.opera_conversation.refresh_token,
            "scope": "shodan:aria user:read"
        }
        response = self.session.post(self.token_endpoint, headers=headers, data=data, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        self.opera_conversation.update_token(
            access_token=result["access_token"],
            expires_in=result.get("expires_in", 3600)
        )
        return result["access_token"]

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: Optional[str] = None,
        conversationally: bool = False,
        **kwargs: Any,
    ) -> Response:

        conversation_prompt = self.conversation.gen_complete_prompt(prompt)

        try:
            access_token = self._get_access_token()
        except Exception as e:
            raise exceptions.FailedToGenerateResponseError(f"Failed to auth OperaAria: {e}")

        headers = {
            "Accept": "text/event-stream" if stream else "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Origin": "opera-aria://ui",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
        }

        data = {
            "query": conversation_prompt if conversationally else prompt,
            "stream": stream,
            "linkify": True,
            "linkify_version": 3,
            "sia": True,
            "media_attachments": [],
            "encryption": {"key": self.opera_conversation.encryption_key}
        }

        if not self.opera_conversation.is_first_request and self.opera_conversation.conversation_id:
            data["conversation_id"] = self.opera_conversation.conversation_id

        def for_stream():
            try:
                with Session(impersonate="chrome110") as __sess:
                    response = __sess.post(
                    self.api_endpoint,
                    headers=headers,
                    json=data,
                    stream=True,
                    timeout=self.timeout

                )
                response.raise_for_status()

                full_message = ""
                for line in response.iter_lines():
                    if not line:
                        continue
                    decoded = line.decode('utf-8').strip()
                    if not decoded.startswith('data: '):
                        continue

                    content = decoded[6:]
                    if content == '[DONE]':
                        break

                    try:
                        json_data = json.loads(content)
                        if 'message' in json_data:
                            msg_chunk = json_data['message']
                            full_message += msg_chunk
                            if raw:
                                yield msg_chunk
                            else:
                                yield dict(text=msg_chunk)
                    except json.JSONDecodeError:
                        continue

                self.opera_conversation.is_first_request = False

                self.conversation.update_chat_history(
                    prompt, full_message
                )

            except RequestException as e:
                raise exceptions.FailedToGenerateResponseError(f"Request failed (RequestException): {e}") from e
            except Exception as e:
                raise exceptions.FailedToGenerateResponseError(f"Request failed: {e}") from e

        def for_non_stream():
            try:
                response = self.session.post(
                    self.api_endpoint,
                    headers=headers,
                    json=data,
                    stream=False,
                    timeout=self.timeout

                )
                response.raise_for_status()

                json_data = response.json()
                message = json_data.get('message', '')

                self.opera_conversation.is_first_request = False
                self.conversation.update_chat_history(prompt, message)

                if raw:
                    return message
                return dict(text=message)

            except RequestException as e:
                raise exceptions.FailedToGenerateResponseError(f"Request failed (RequestException): {e}") from e
            except Exception as e:
                raise exceptions.FailedToGenerateResponseError(f"Request failed: {e}") from e

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: Optional[str] = None,
        conversationally: bool = False,
        **kwargs: Any,
    ) -> Union[str, Generator[str, None, None]]:

        def generator():
            chat_response = self.ask(
                prompt, True, raw=False, optimizer=optimizer, conversationally=conversationally, **kwargs
            )
            for chunk in chat_response:
                yield self.get_message(chunk)

        if stream:
            return generator()

        chat_response = self.ask(
            prompt, False, raw=False, optimizer=optimizer, conversationally=conversationally, **kwargs
        )
        return self.get_message(chat_response)

    def get_message(self, response: Response) -> str:
        if not isinstance(response, dict):
            return str(response)
        return cast(Dict[str, Any], response).get("text", "")
