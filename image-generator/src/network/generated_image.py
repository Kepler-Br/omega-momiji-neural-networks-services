from dataclasses import dataclass


@dataclass
class GeneratedImage:
    # base64 PNG image
    image: str
