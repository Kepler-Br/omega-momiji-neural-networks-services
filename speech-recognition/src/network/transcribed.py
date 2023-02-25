from dataclasses import dataclass
from typing import Optional


@dataclass
class Transcribed:
    language: str
    text: str
