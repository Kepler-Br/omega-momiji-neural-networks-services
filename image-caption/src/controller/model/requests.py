from typing import Optional

from pydantic import BaseModel, Field


class ControllerRequest(BaseModel):
    data: str = Field(min_length=1)
    condition: Optional[str] = Field(None)

    class Config:
        use_enum_values = True
