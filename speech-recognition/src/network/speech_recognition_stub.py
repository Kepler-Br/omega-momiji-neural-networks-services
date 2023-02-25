import logging
from abc import abstractmethod
from typing import Tuple, Optional

from network.speech_recognition_abstract import SpeechRecognitionAbstract
from network.transcribed import Transcribed


class SpeechRecognitionStub(SpeechRecognitionAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def transcribe(
            self,
            audio_bytes: bytes,
            temperature: float | Tuple[float, ...] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            beam_size: Optional[int] = None,
            patience: Optional[float] = None,
            best_of: Optional[int] = None,
    ) -> Transcribed:
        self.log.debug(f'(Stub) Transcribing audio:\n'
                       f'Audio size: {len(audio_bytes)} bytes\n'
                       f'Temperature: {temperature}\n'
                       f'Beam size: {beam_size}\n'
                       f'Patience: {patience}\n'
                       f'Best of: {best_of}')

        return Transcribed(
            language='bee',
            text='According to all known laws of aviation, there is no way that a bee should be able to fly. '
                 'Its wings are too small to get its fat little body off the ground. '
                 'The bee, of course, flies anyways.',
        )
