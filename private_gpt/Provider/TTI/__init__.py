# This file marks the directory as a Python package.
# Static imports for all TTI (Text-to-Image) provider modules

# Base classes
from private_gpt.Provider.TTI.base import (
    BaseImages,
    TTICompatibleProvider,
)

# Provider implementations
from private_gpt.Provider.TTI.magicstudio import MagicStudioAI
from private_gpt.Provider.TTI.miragic import MiragicAI
from private_gpt.Provider.TTI.pollinations import PollinationsAI
from private_gpt.Provider.TTI.together import TogetherImage

# Utility classes
from private_gpt.Provider.TTI.utils import (
    ImageData,
    ImageResponse,
)

# List of all exported names
__all__ = [
    # Base classes
    "TTICompatibleProvider",
    "BaseImages",
    # Utilities
    "ImageData",
    "ImageResponse",
    # Providers
    "MagicStudioAI",
    "PollinationsAI",
    "TogetherImage",
    "MiragicAI",
]
