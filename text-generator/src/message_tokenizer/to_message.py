from typing import Iterable

from controller.model.message import Message, MessageType
from message_tokenizer.tokens import Token, MessageIdToken, MessageBodyToken, ReplyToToken, FromToken


class InvalidTokenSeq(RuntimeError):
    pass


def _split_tokens_into_batches(tokens: Iterable[Token]) -> list[tuple[MessageIdToken | Token, ...]]:
    split = []

    accumulated = []
    for p in tokens:
        if isinstance(p, MessageIdToken) and len(accumulated) != 0:
            split.append(tuple(accumulated))
            accumulated = []
        accumulated.append(p)

    if len(accumulated) != 0 and isinstance(accumulated[-1], MessageBodyToken):
        split.append(tuple(accumulated))

    return split


def _token_batch_to_message(batch: Iterable[Token]) -> Message:
    message_id = None
    reply_to = None
    username = None
    message_body = None

    for token in batch:
        token: Token

        if isinstance(token, MessageIdToken):
            token: MessageIdToken
            message_id = int(token.val)

        if isinstance(token, MessageBodyToken):
            token: MessageBodyToken
            message_body = token.val

        if isinstance(token, ReplyToToken):
            token: ReplyToToken
            reply_to = int(token.val)

        if isinstance(token, FromToken):
            token: FromToken
            username = token.val
    if message_id is None or username is None or message_body is None:
        raise InvalidTokenSeq(f'One of message id({message_id}) '
                              f'or username({username}) '
                              f'or message body({message_body}) is None')

    return Message(
        message_type=MessageType.TEXT,
        content=message_body,
        author=username,
        message_id=message_id,
        reply_to_message_id=reply_to,
        emoji=None,
    )


def map_tokens_to_messages(tokens: Iterable[Token]) -> list[Message]:
    split = _split_tokens_into_batches(tokens)
    ret = []
    for batch in split:
        try:
            ret.append(_token_batch_to_message(batch))
        except InvalidTokenSeq as e:
            print(e)
            continue
    return ret
