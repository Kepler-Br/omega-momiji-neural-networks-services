from typing import Optional

from pydantic import BaseModel, Field

from controller.model.enums import MessageType


class Message(BaseModel):
    message_type: MessageType = Field()
    content: str = Field()
    author: str = Field()
    message_id: str = Field()
    reply_to_message_id: Optional[str] = Field(None)
    emoji: Optional[str] = Field(None)

    class Config:
        use_enum_values = True
