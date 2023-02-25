from typing import Tuple

from pydantic import BaseModel, Field


class SpeechRecognizeRequest(BaseModel):
    audio: str = Field(min_length=1)
    temperature: float | Tuple[float, ...] = Field([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    beam_size: int = Field(None, gt=0)
    patience: float = Field(None)
    best_of: int = Field(None, gt=1)
