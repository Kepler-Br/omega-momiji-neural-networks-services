import logging
from io import BytesIO
from typing import Optional

from PIL import Image

from app_stuff import ModelType
from clip_interrogator import Interrogator, Config
from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract
from network.utils import fill_alpha_with_color


class ClipInterrogatorNeuralNetwork(CaptioningNeuralNetworkAbstract):
    def __init__(
            self,
            clip_name: str,
            caption_name: str,
            chunk_size: int,
            caption_max_length: int = 32,
            device_override: Optional[str] = None,
    ):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self.device_override = device_override
        self.log.info('Loading interrogator')
        self.interrogator = Interrogator(
            Config(
                clip_model_name=clip_name,
                chunk_size=chunk_size,
                caption_model_name=caption_name,
                caption_max_length=caption_max_length,
                device='cpu' if device_override is None else device_override,
                quiet=True,
            )
        )
        self.log.info('Done')

    def caption(
            self,
            image: bytes,
            condition: Optional[str] = None,
    ) -> str:
        self.log.info(
            f'Caption image:\n'
            f'Bytes total: {len(image)}\n'
            f'Condition: "{condition}"'
        )

        raw_image = fill_alpha_with_color(Image.open(BytesIO(image))).convert('RGB')

        processed = self.interrogator.interrogate(image=raw_image)

        self.log.info(f'Image processed. Caption: "{processed}"')

        return processed

    def name(self) -> str:
        return ModelType.CLIP_INTERROGATOR
