import logging
from typing import Optional

from controller.model.history_generation_request import GenerationParams
from controller.model.message import Message, MessageType
from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract
from network.messages_to_prompt import messages_to_prompt


class LanguageNeuralNetworkStub(LanguageNeuralNetworkAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def generate(
            self,
            prompt: str,
            generation_params: GenerationParams,
            count: int = 1,
    ) -> list[str]:
        self.log.debug(
            f'(Stub) Generating text:\n'
            f'Prompt: {prompt}\n'
            f'Count: {count}\n'
            f'Max new tokens: {generation_params.max_new_tokens}\n'
            f'Num beams: {generation_params.num_beams}\n'
            f'No repeat ngram size: {generation_params.no_repeat_ngram_size}\n'
            f'Repetition penalty: {generation_params.repetition_penalty}\n'
            f'Early stopping: {generation_params.early_stopping}\n'
            f'Seed: {generation_params.seed}\n'
            f'Top k: {generation_params.top_k}\n'
            f'Top p: {generation_params.top_p}\n'
            f'Temperature: {generation_params.temperature}\n'
            f'Bad words: {generation_params.bad_words}\n'
        )
        return ['According to all known laws of aviation, there is no way that a bee should be able to fly. '
                'Its wings are too small to get its fat little body off the ground. '
                'The bee, of course, flies anyways.']

    def generate_messages(
            self,
            messages: list[Message],
            generation_params: GenerationParams,
            prompt_author: str,
            reply_to_id: Optional[int] = None,
            prompt: Optional[str] = None,
    ) -> list[Message]:
        messages_as_prompt = messages_to_prompt(messages)

        self.log.debug(
            f'(Stub) Generating messages:\n'
            f'Prompt: {messages_as_prompt}\n'
            f'Max new tokens: {generation_params.max_new_tokens}\n'
            f'Num beams: {generation_params.num_beams}\n'
            f'No repeat ngram size: {generation_params.no_repeat_ngram_size}\n'
            f'Repetition penalty: {generation_params.repetition_penalty}\n'
            f'Early stopping: {generation_params.early_stopping}\n'
            f'Seed: {generation_params.seed}\n'
            f'Top k: {generation_params.top_k}\n'
            f'Top p: {generation_params.top_p}\n'
            f'Temperature: {generation_params.temperature}\n'
            f'Bad words: {generation_params.bad_words}\n'
        )

        last_message_id = messages[-1].message_id

        return [
            Message(
                message_type=MessageType.TEXT,
                content='According to all known laws of aviation, there is no way that a bee should be able to fly',
                author=prompt_author,
                message_id=last_message_id + '1',
            ),
            Message(
                message_type=MessageType.TEXT,
                content='Its wings are too small to get its fat little body off the ground',
                author=prompt_author,
                message_id=last_message_id + '2',
            ),
            Message(
                message_type=MessageType.TEXT,
                content='The bee, of course, flies anyways',
                author=f'{prompt_author} Stub',
                message_id=last_message_id + '3',
            ),
        ]
