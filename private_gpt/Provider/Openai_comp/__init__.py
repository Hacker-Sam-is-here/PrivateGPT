# This file marks the directory as a Python package.
# Static imports for all Openai_comp provider modules

# Base classes and utilities
from private_gpt.Provider.Openai_comp.ai4chat import AI4Chat
from private_gpt.Provider.Openai_comp.akashgpt import AkashGPT
from private_gpt.Provider.Openai_comp.avasupernova import AvaSupernova
from private_gpt.Provider.Openai_comp.ayle import Ayle
from private_gpt.Provider.Openai_comp.base import (
    BaseChat,
    BaseCompletions,
    FunctionDefinition,
    FunctionParameters,
    OpenAICompatibleProvider,
    SimpleModelList,
    Tool,
    ToolDefinition,
)
from private_gpt.Provider.Openai_comp.cerebras import Cerebras
from private_gpt.Provider.Openai_comp.chatgpt import ChatGPT, ChatGPTReversed
from private_gpt.Provider.Openai_comp.copilot import Copilot

# Provider implementations
from private_gpt.Provider.Openai_comp.DeepAI import DeepAI
from private_gpt.Provider.Openai_comp.deepinfra import DeepInfra
from private_gpt.Provider.Openai_comp.e2b import E2B
from private_gpt.Provider.Openai_comp.elmo import Elmo
from private_gpt.Provider.Openai_comp.exaai import ExaAI
from private_gpt.Provider.Openai_comp.freeassist import FreeAssist
from private_gpt.Provider.Openai_comp.groq import Groq
from private_gpt.Provider.Openai_comp.heckai import HeckAI
from private_gpt.Provider.Openai_comp.huggingface import HuggingFace
from private_gpt.Provider.Openai_comp.ibm import IBM
from private_gpt.Provider.Openai_comp.k2think import K2Think
from private_gpt.Provider.Openai_comp.llmchat import LLMChat
from private_gpt.Provider.Openai_comp.llmchatco import LLMChatCo
from private_gpt.Provider.Openai_comp.meta import Meta
from private_gpt.Provider.Openai_comp.netwrck import Netwrck
from private_gpt.Provider.Openai_comp.nvidia import Nvidia
from private_gpt.Provider.Openai_comp.openrouter import OpenRouter
from private_gpt.Provider.Openai_comp.PI import PiAI
from private_gpt.Provider.Openai_comp.sambanova import Sambanova
from private_gpt.Provider.Openai_comp.sonus import SonusAI
from private_gpt.Provider.Openai_comp.textpollinations import TextPollinations
from private_gpt.Provider.Openai_comp.TogetherAI import TogetherAI
from private_gpt.Provider.Openai_comp.toolbaz import Toolbaz
from private_gpt.Provider.Openai_comp.TwoAI import TwoAI
from private_gpt.Provider.Openai_comp.typliai import TypliAI
from private_gpt.Provider.Openai_comp.upstage import Upstage
from private_gpt.Provider.Openai_comp.venice import Venice
from private_gpt.Provider.Openai_comp.utils import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    Choice,
    ChoiceDelta,
    CompletionUsage,
    FunctionCall,
    ModelData,
    ModelList,
    ToolCall,
    ToolCallType,
    ToolFunction,
    count_tokens,
    format_prompt,
    get_last_user_message,
    get_system_prompt,
)
from private_gpt.Provider.Openai_comp.wisecat import WiseCat
from private_gpt.Provider.Openai_comp.writecream import Writecream
from private_gpt.Provider.Openai_comp.qwenchat import QwenChat
from private_gpt.Provider.Openai_comp.zenmux import Zenmux

# List of all exported names
__all__ = [
    # Base classes and utilities
    "OpenAICompatibleProvider",
    "SimpleModelList",
    "BaseChat",
    "BaseCompletions",
    "Tool",
    "ToolDefinition",
    "FunctionParameters",
    "FunctionDefinition",
    # Utils
    "ChatCompletion",
    "ChatCompletionChunk",
    "Choice",
    "ChoiceDelta",
    "ChatCompletionMessage",
    "CompletionUsage",
    "ToolCall",
    "ToolFunction",
    "FunctionCall",
    "ToolCallType",
    "ModelData",
    "ModelList",
    "format_prompt",
    "get_system_prompt",
    "get_last_user_message",
    "count_tokens",
    # Provider implementations
    "Copilot",
    "DeepAI",
    "PiAI",
    "TogetherAI",
    "TwoAI",
    "AI4Chat",
    "AkashGPT",
    "Cerebras",
    "ChatGPT",
    "ChatGPTReversed",
    "DeepInfra",
    "E2B",
    "Elmo",
    "ExaAI",
    "FreeAssist",
    "Ayle",
    "HuggingFace",
    "Groq",
    "HeckAI",
    "IBM",
    "K2Think",
    "LLMChat",
    "LLMChatCo",
    "Netwrck",
    "Nvidia",
    "OpenRouter",
    "SonusAI",
    "TextPollinations",
    "AvaSupernova",
    "Toolbaz",
    "Upstage",
    "WiseCat",
    "QwenChat",
    "Writecream",
    "YEPCHAT",
    "Zenmux",
    "Sambanova",
    "Meta",
    "TypliAI",
    "Venice",
]

# --- Dynamic Legacy Providers Loading ---
try:
    from private_gpt.AIauto import load_providers
    from private_gpt.Provider.Openai_comp.legacy_adapters import create_adapter

    # Load all standard providers not natively in Openai_comp
    provider_map, _ = load_providers()
    _globals = globals()

    for _name, _provider_cls in provider_map.items():
        # Avoid overriding existing native wrappers in Openai_comp
        real_name = getattr(_provider_cls, "__name__", _name)
        if real_name not in _globals:
            adapted_cls = create_adapter(_provider_cls)
            _globals[real_name] = adapted_cls
            if "__all__" in _globals:
                _globals["__all__"].append(real_name)
except Exception as e:
    from litprinter import ic
    ic.configureOutput(prefix='WARNING| ')
    ic(f"Failed to dynamically load legacy providers: {e}")
