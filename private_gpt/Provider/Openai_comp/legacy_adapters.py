import time
import uuid
from typing import Any, Dict, Generator, List

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
)


class LegacyCompletions(BaseCompletions):
    def __init__(self, client):
        self._client = client

    def create(self, *, model: str, messages: List[Dict[str, str]], stream: bool = False, **kwargs):
        prompt = ""
        system = ""
        for m in messages:
            role = m.get("role", "")
            if role == "system":
                system = m.get("content", "")
            else:
                prompt += f"{role.capitalize()}: {m.get('content', '')}\n"
        prompt += "Assistant: "

        provider_kwargs = getattr(self._client, "init_kwargs", {}).copy()

        # Inject system prompt if supported
        try:
            import inspect

            sig = inspect.signature(self._client.legacy_class.__init__)
            if "system_prompt" in sig.parameters:
                provider_kwargs["system_prompt"] = system if system else "You are a helpful AI"
        except Exception:
            pass

        provider_instance = self._client.legacy_class(model=model, **provider_kwargs)

        if stream:
            return self._stream_response(provider_instance, prompt, model)
        else:
            return self._sync_response(provider_instance, prompt, model)

    def _sync_response(self, provider_instance, prompt, model):
        try:
            resp = provider_instance.chat(prompt, stream=False)
            if isinstance(resp, Generator) or (
                hasattr(resp, "__iter__")
                and getattr(resp, "__name__", "") != "str"
                and not isinstance(resp, str)
            ):
                # If it still returned a generator somehow
                resp = "".join(list(resp))
        except Exception as e:
            raise Exception(f"Provider request failed: {e}")

        completion_id = f"chatcmpl-{uuid.uuid4()}"
        created = int(time.time())
        return ChatCompletion(
            id=completion_id,
            choices=[
                Choice(
                    finish_reason="stop",
                    index=0,
                    message=ChatCompletionMessage(content=str(resp), role="assistant"),
                )
            ],
            created=created,
            model=model,
            object="chat.completion",
            system_fingerprint="fp_legacy",
        )

    def _stream_response(self, provider_instance, prompt, model):
        try:
            gen = provider_instance.chat(prompt, stream=True)
        except Exception as e:
            raise Exception(f"Provider request failed: {e}")

        completion_id = f"chatcmpl-{uuid.uuid4()}"
        created = int(time.time())

        try:
            for chunk in gen:
                yield ChatCompletionChunk(
                    id=completion_id,
                    choices=[
                        Choice(
                            delta=ChoiceDelta(content=str(chunk), role="assistant"),
                            finish_reason=None,
                            index=0,
                        )
                    ],
                    created=created,
                    model=model,
                    object="chat.completion.chunk",
                    system_fingerprint="fp_legacy",
                )
        except Exception as e:
            # Yield error in chunk if possible
            yield ChatCompletionChunk(
                id=completion_id,
                choices=[
                    Choice(
                        delta=ChoiceDelta(content=f"\n[Error: {str(e)}]", role="assistant"),
                        finish_reason="error",
                        index=0,
                    )
                ],
                created=created,
                model=model,
                object="chat.completion.chunk",
                system_fingerprint="fp_legacy",
            )


class LegacyChat(BaseChat):
    def __init__(self, client):
        self.completions = LegacyCompletions(client)


class LegacyAdapter(OpenAICompatibleProvider):
    AVAILABLE_MODELS = []
    legacy_class: Any = None
    required_auth = False

    def __init__(self, **kwargs):
        self.init_kwargs = kwargs
        self.chat = LegacyChat(self)

    @property
    def models(self):
        return SimpleModelList(getattr(self.__class__, "AVAILABLE_MODELS", []))


def create_adapter(legacy_cls):
    """Creates a dynamic OpenAICompatibleProvider from a legacy Provider."""

    class AdaptedProvider(LegacyAdapter):
        AVAILABLE_MODELS = getattr(legacy_cls, "AVAILABLE_MODELS", [])
        legacy_class = legacy_cls
        required_auth = getattr(legacy_cls, "required_auth", False)

    AdaptedProvider.__name__ = f"{legacy_cls.__name__}"
    return AdaptedProvider
