from controller.model.message import Message


class MessageIdMapper:
    def __init__(self):
        self.ids_to_index: dict[str, str] = dict()
        self.index_to_ids: dict[str, str] = dict()

    def map_and_save_ids(self, messages: list[Message]) -> list[Message]:
        self.ids_to_index = dict(
            zip(
                map(lambda x: x.message_id, messages),
                map(lambda x: str(x), range(1, len(messages) + 1))
            )
        )

        self.index_to_ids = dict(
            zip(
                map(lambda x: str(x), range(1, len(messages) + 1)),
                map(lambda x: x.message_id, messages),
            )
        )

        mapped = map(
            lambda x: x.copy(update={
                'message_id':
                    self.ids_to_index[x.message_id],
                'reply_to_message_id':
                    None if x.reply_to_message_id is None else self.ids_to_index.get(x.reply_to_message_id, '0')
            }),
            messages
        )

        return [*mapped]

    def map_to_original_ids(self, messages: list[Message]) -> list[Message]:
        mapped = map(
            lambda x: x.copy(update={
                'message_id':
                    self.index_to_ids.get(x.message_id, x.message_id),
                'reply_to_message_id':
                    None if x.reply_to_message_id is None else self.index_to_ids.get(x.reply_to_message_id, None)
            }),
            messages
        )

        return [*mapped]
