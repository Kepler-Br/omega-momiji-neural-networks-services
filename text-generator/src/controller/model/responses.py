from typing import Optional

from pydantic import BaseModel, Field

from controller.model.message import Message


class ResponseStatus:
    OK = 'OK'
    TOO_EARLY = 'TOO_EARLY'
    BAD_REQUEST = 'BAD_REQUEST'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    NOT_FOUND = 'NOT_FOUND'


class HistoryGenerationResponse(BaseModel):
    status: Optional[str] = Field(None)
    messages: Optional[list[Message]] = Field()
    error_message: Optional[str] = Field(None)


class BasicResponse(BaseModel):
    status: Optional[str] = Field(None)
    error_message: Optional[str] = Field(None)
