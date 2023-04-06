from typing import Optional

from pydantic import BaseModel, Field

from controller.model.enums import ResponseStatus
from controller.model.message import Message


class BasicResponse(BaseModel):
    status: ResponseStatus = Field(None)
    error_message: Optional[str] = Field(None)

    class Config:
        use_enum_values = True


class HistoryGenerationResponse(BasicResponse):
    messages: Optional[list[Message]] = Field()

    class Config:
        use_enum_values = True


class TextScheduledResponse(BasicResponse):
    task_id: Optional[str] = Field(None)

    class Config:
        use_enum_values = True
