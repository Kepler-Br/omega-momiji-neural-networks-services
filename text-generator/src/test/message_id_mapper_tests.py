import unittest

from controller.model.message import Message
from util.message_id_mapper import MessageIdMapper


class MessageIdMapperTests(unittest.TestCase):
    @staticmethod
    def get_test_data() -> list[Message]:
        return [
            Message(
                message_type='TEXT',
                content='content',
                author='author',
                message_id='message_id_1',
                reply_to_message_id='message_id_unknown',
            ),
            Message(
                message_type='TEXT',
                content='content',
                author='author2',
                message_id='message_id_2',
                reply_to_message_id='message_id_1',
            ),
        ]

    def test_messages_mapped_back(self):
        messages: list[Message] = self.get_test_data()

        mapper = MessageIdMapper()
        mapped_messages = mapper.map_and_save_ids(messages)
        mapped_messages[0].reply_to_message_id = 'UNKNOWN GENERATED MESSAGE ID'
        mapped_messages[0].message_id = 'UNKNOWN GENERATED MESSAGE ID'
        mapped_back_messages = mapper.map_to_original_ids(mapped_messages)

        self.assertEqual(
            mapped_back_messages[0].message_id,
            'UNKNOWN GENERATED MESSAGE ID',
            msg='Unknown messages in id should be left as is'
        )
        self.assertIsNone(
            mapped_back_messages[0].reply_to_message_id,
            msg='Unknown messages in reply should be None'
        )

        self.assertEqual(
            mapped_back_messages[1].message_id,
            'message_id_2',
        )
        self.assertEqual(
            mapped_back_messages[1].reply_to_message_id,
            'message_id_1',
        )

    def test_messages_mapped_to_indexes(self):
        messages: list[Message] = self.get_test_data()

        mapper = MessageIdMapper()
        mapped_messages = mapper.map_and_save_ids(messages)

        self.assertEqual(
            mapped_messages[0].message_id,
            '1',
            msg='First message should be 1'
        )
        self.assertEqual(
            mapped_messages[0].reply_to_message_id,
            '0',
            msg='Unknown message id is not 0'
        )

        self.assertEqual(
            mapped_messages[1].message_id,
            '2',
        )
        self.assertEqual(
            mapped_messages[1].reply_to_message_id,
            '1',
        )


if __name__ == '__main__':
    unittest.main()
