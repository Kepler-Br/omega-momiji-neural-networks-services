import inspect
from abc import ABC, abstractmethod

from network.captioned import Captioned


class ImageCaptioningAbstract(ABC):
    @abstractmethod
    def caption(
            self,
            image_bytes: bytes,
    ) -> Captioned:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
