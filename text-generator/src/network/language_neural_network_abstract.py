import inspect
from abc import ABC, abstractmethod
from typing import Optional

from controller.model.history_generation_request import GenerationParams
from controller.model.message import Message


class LanguageNeuralNetworkAbstract(ABC):
    @abstractmethod
    def generate(
            self,
            prompt: str,
            generation_params: GenerationParams,
            count: int = 1,
    ) -> list[str]:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')

    @abstractmethod
    def generate_messages(
            self,
            messages: list[Message],
            generation_params: GenerationParams,
            prompt_author: str,
            reply_to_id: Optional[int] = None,
            prompt: Optional[str] = None,
    ) -> list[Message]:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
