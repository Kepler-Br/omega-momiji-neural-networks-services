from typing import Optional

from pydantic import BaseModel, Field


class GeneratedResponse(BaseModel):
    text: Optional[list[str]] = Field(None)
    error_message: Optional[str] = Field(None)
