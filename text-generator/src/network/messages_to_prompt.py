import inspect
from typing import Iterable, Optional

from controller.model.message import Message, MessageType
from message_tokenizer.tokenizer import data_to_tokenized_text


def _map_message_to_text(value: Message) -> str:
    if value.message_type == MessageType.TEXT:
        return value.content
    if value.message_type == MessageType.IMAGE:
        return '[IMAGE]'
    if value.message_type == MessageType.VOICE:
        return '[VOICE]'
    if value.message_type == MessageType.STICKER:
        return '[STICKER]'

    raise RuntimeError(f'{inspect.stack()[0][3]}: unmapped message type enum: {value.message_type}')


def messages_to_prompt(messages: Iterable[Message]) -> str:
    message_prompt_list: list[str] = []

    for message in messages:
        message_prompt_list.append(
            data_to_tokenized_text(
                message_id=message.message_id,
                text=_map_message_to_text(message),
                author=message.author,
                reply_to_message=message.reply_to_message_id,
            )
        )

    return '\n'.join(message_prompt_list)
