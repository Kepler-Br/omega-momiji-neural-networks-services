import logging
from io import BytesIO
from typing import Optional

from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract


class Blip2CaptioningNeuralNetwork(CaptioningNeuralNetworkAbstract):
    def __init__(self, path: str, device_override: Optional[str] = None):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self.device_override = device_override
        self.log.info('Loading processor')
        self.processor = Blip2Processor.from_pretrained(path)
        self.log.info('Loading model')
        self.model = Blip2ForConditionalGeneration.from_pretrained(path)

        if self.device_override is not None:
            self.log.info(f'Moving model to device {device_override}')
            self.processor = self.processor.to(device_override)
            self.model = self.model.to(device_override)

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
        raw_image = Image.open(BytesIO(image)).convert('RGB')

        inputs = self.processor(raw_image, condition, return_tensors="pt")

        out = self.model.generate(**inputs, max_new_tokens=500)
        processed = self.processor.decode(out[0], skip_special_tokens=True).strip()

        self.log.info(f'Image processed. Caption: "{processed}"')

        return processed
