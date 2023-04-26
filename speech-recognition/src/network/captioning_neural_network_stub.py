import logging

from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract


class CaptioningNeuralNetworkStub(CaptioningNeuralNetworkAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def caption(
            self,
            voice: bytes,
    ) -> str:
        self.log.debug(
            f'(Stub) Recognize voice:\n'
            f'Bytes total: {len(voice)}'
        )

        return 'According to all known laws of aviation, there is no way that a bee should be able to fly. ' + \
            'Its wings are too small to get its fat little body off the ground. ' + \
            'The bee, of course, flies anyways.'
