from typing import Optional

from pydantic import BaseModel, Field

from controller.model.enums import ResponseStatus


class BaseResponse(BaseModel):
    status: ResponseStatus = Field(None)
    error_message: Optional[str] = Field(None)

    class Config:
        use_enum_values = True


class CaptionResponse(BaseResponse):
    caption: Optional[str] = Field()

    class Config:
        use_enum_values = True


class CaptioningScheduledResponse(BaseResponse):
    task_id: Optional[str] = Field(None)

    class Config:
        use_enum_values = True
