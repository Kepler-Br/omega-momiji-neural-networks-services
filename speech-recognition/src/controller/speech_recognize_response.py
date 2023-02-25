from typing import Optional

from pydantic import BaseModel, Field


class SpeechRecognizeResponse(BaseModel):
    text: Optional[str] = Field(None)
    language: Optional[str] = Field(None)
    error_message: Optional[str] = Field(None)
