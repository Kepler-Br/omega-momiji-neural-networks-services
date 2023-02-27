from typing import Optional

from pydantic import BaseModel, Field


class ControllerResponse(BaseModel):
    text: Optional[str] = Field(None)
    error_message: Optional[str] = Field(None)
