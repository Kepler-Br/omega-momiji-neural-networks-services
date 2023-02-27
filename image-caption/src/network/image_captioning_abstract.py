from abc import ABC, abstractmethod

from network.captioned import Captioned


class ImageCaptioningAbstract(ABC):
    @abstractmethod
    def caption(
            self,
            image_bytes: bytes,
    ) -> Captioned:
        raise NotImplementedError(f'caption is not implemented')
