import inspect
from abc import ABC, abstractmethod
from typing import Optional


class CaptioningNeuralNetworkAbstract(ABC):
    @abstractmethod
    def caption(
            self,
            image: bytes,
            condition: Optional[str] = None,
    ) -> str:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
