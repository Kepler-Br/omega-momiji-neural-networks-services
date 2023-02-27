from pydantic import BaseModel, Field


class ControllerRequest(BaseModel):
    image: str = Field(min_length=1)
