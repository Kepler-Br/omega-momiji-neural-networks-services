from typing import Optional, List

from pydantic import BaseModel, Field


# region generate text
class GenerateTextRequest(BaseModel):
    text: str = Field()
    max_length: int = Field()


class GenerateTextErrorResponse(BaseModel):
    error_message: str = Field()
    error_code: str = Field()


class GenerateTextResponse(BaseModel):
    text: str = Field()
    finish_reason: str = Field()


# endregion generate text

# region generate message
class Message(BaseModel):
    id: str = Field()
    username: str = Field()
    text: Optional[str] = Field(None)
    media_type: Optional[str] = Field(None)
    media_caption: Optional[str] = Field(None)
    reply_to: Optional[str] = Field(None)


class GenerateMessageRequest(BaseModel):
    messages: List[Message] = Field()
    prompt: str = Field()
    pre_prompt: Optional[str] = Field(None)
    max_length: int = Field()


class GeneratedMessages(BaseModel):
    text: str = Field()
    reply_to: Optional[str] = Field(None)


class GenerateMessageResponse(BaseModel):
    messages: List[GeneratedMessages] = Field()
# endregion generate message
