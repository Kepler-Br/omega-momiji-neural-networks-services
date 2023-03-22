from typing import Optional

from pydantic import BaseModel, Field


class MessageType:
    VOICE = 'VOICE'
    IMAGE = 'IMAGE'
    STICKER = 'STICKER'
    TEXT = 'TEXT'


class Message(BaseModel):
    message_type: str = Field()
    content: str = Field()
    author: str = Field()
    message_id: int = Field()
    reply_to_message_id: Optional[int] = Field(None)
    emoji: Optional[str] = Field(None)
