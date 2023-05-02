import logging
from typing import Optional

from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract

from app_stuff import ModelType


class CaptioningNeuralNetworkStub(CaptioningNeuralNetworkAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def caption(
            self,
            image: bytes,
            condition: Optional[str] = None,
    ) -> str:
        self.log.info(
            f'(Stub) Caption image:\n'
            f'Bytes total: {len(image)}'
            f'Condition: "{condition}"'
        )

        return 'According to all known laws of aviation, there is no way that a bee should be able to fly. ' + \
            'Its wings are too small to get its fat little body off the ground. ' + \
            'The bee, of course, flies anyways.'

    def name(self) -> str:
        return ModelType.STUB
