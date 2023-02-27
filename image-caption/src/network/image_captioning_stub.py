import logging

from network.captioned import Captioned
from network.image_captioning_abstract import ImageCaptioningAbstract


class ImageCaptioningStub(ImageCaptioningAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def caption(
            self,
            image_bytes: bytes,
    ) -> Captioned:
        self.log.debug(f'(Stub) Captioned image:\n'
                       f'Image size: {len(image_bytes)} bytes\n'
                       )

        return Captioned(
            text='According to all known laws of aviation, there is no way that a bee should be able to fly. '
                 'Its wings are too small to get its fat little body off the ground. '
                 'The bee, of course, flies anyways.',
        )
