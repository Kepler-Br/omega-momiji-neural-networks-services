import inspect
from abc import ABC, abstractmethod

from network.generated_image import GeneratedImage


class ImageGeneratorAbstract(ABC):
    @abstractmethod
    def generate_image(
            self,
            prompt: str,
            negative_prompt: str,
    ) -> GeneratedImage:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
