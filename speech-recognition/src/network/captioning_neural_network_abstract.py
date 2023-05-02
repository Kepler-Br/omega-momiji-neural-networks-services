import inspect
from abc import ABC, abstractmethod


class CaptioningNeuralNetworkAbstract(ABC):
    @abstractmethod
    def caption(
            self,
            voice: bytes,
    ) -> str:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
