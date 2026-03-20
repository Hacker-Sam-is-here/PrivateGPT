# This file marks the directory as a Python package.
# Static imports for all TTS (Text-to-Speech) provider modules

# Base classes
from private_gpt.Provider.TTS.base import (
    AsyncBaseTTSProvider,
    BaseTTSProvider,
)

# Provider implementations
from private_gpt.Provider.TTS.deepgram import DeepgramTTS
from private_gpt.Provider.TTS.elevenlabs import ElevenlabsTTS
from private_gpt.Provider.TTS.freetts import FreeTTS
from private_gpt.Provider.TTS.murfai import MurfAITTS
from private_gpt.Provider.TTS.openai_fm import OpenAIFMTTS
from private_gpt.Provider.TTS.parler import ParlerTTS
from private_gpt.Provider.TTS.pockettts import PocketTTS
from private_gpt.Provider.TTS.qwen import QwenTTS
from private_gpt.Provider.TTS.sherpa import SherpaTTS
from private_gpt.Provider.TTS.speechma import SpeechMaTTS
from private_gpt.Provider.TTS.streamElements import StreamElements

# Utility classes
from private_gpt.Provider.TTS.utils import SentenceTokenizer

# List of all exported names
__all__ = [
    # Base classes
    "BaseTTSProvider",
    "AsyncBaseTTSProvider",
    # Utilities
    "SentenceTokenizer",
    # Providers
    "DeepgramTTS",
    "ElevenlabsTTS",
    "FreeTTS",
    "MurfAITTS",
    "OpenAIFMTTS",
    "ParlerTTS",
    "PocketTTS",
    "QwenTTS",
    "SherpaTTS",
    "SpeechMaTTS",
    "StreamElements",
]
