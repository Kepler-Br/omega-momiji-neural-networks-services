import inspect
from abc import ABC, abstractmethod
from typing import Tuple, Optional

from network.transcribed import Transcribed


class SpeechRecognitionAbstract(ABC):
    @abstractmethod
    def transcribe(
            self,
            audio_bytes: bytes,
            temperature: float | Tuple[float, ...] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            beam_size: Optional[int] = None,
            patience: Optional[float] = None,
            best_of: Optional[int] = None,
    ) -> Transcribed:
        raise NotImplementedError(f'{inspect.stack()[0][3]} is not implemented')
