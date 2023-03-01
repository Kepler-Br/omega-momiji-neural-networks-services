from typing import Optional

from pydantic import BaseModel, Field


class ControllerRequest(BaseModel):
    prompt: str = Field(min_length=1)
    negative_prompt: Optional[str] = Field(None)
