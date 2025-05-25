from abc import ABC, abstractmethod
from typing import Optional, List


class TextPromptWrapper(ABC):
    @abstractmethod
    def get_user_tag(self) -> str:
        pass

    @abstractmethod
    def get_assistant_tag(self) -> str:
        pass

    @abstractmethod
    def get_stop_sequence(self) -> List[str]:
        pass

    @abstractmethod
    def wrap(self, prompt: str, pre_prompt: Optional[str] = None) -> str:
        pass


class MistralV7TextPrompt(TextPromptWrapper):
    def __init__(self):
        self._user_tag = '</s>[INST]'
        self._assistant_tag = '[/INST]'
        self._stop_sequence = [self._user_tag, self._assistant_tag]

    def get_user_tag(self) -> str:
        return self._user_tag

    def get_assistant_tag(self) -> str:
        return self._assistant_tag

    def get_stop_sequence(self) -> List[str]:
        return self._stop_sequence

    def wrap(self, prompt: str, pre_prompt: Optional[str] = None) -> str:
        if pre_prompt is not None:
            return f'{self._user_tag}{prompt}{self._assistant_tag}{pre_prompt}'
        return f'{self._user_tag}{prompt}{self._assistant_tag}'
