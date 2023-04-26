from pydantic import BaseModel, Field


class ControllerRequest(BaseModel):
    data: str = Field(min_length=1)

    class Config:
        use_enum_values = True
