import logging
import time
from typing import Optional, Tuple

import whisper

from load_audio import load_audio
from network.speech_recognition_abstract import SpeechRecognitionAbstract, Transcribed


class SpeechRecognition(SpeechRecognitionAbstract):
    def __init__(
            self,
            model_path: str,
            use_cpu: bool = False,
            use_fp16: bool = False,
            download_root: str = None,
    ):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self.log.debug('Loading model')
        self.model = whisper.load_model(model_path, download_root=download_root)
        self.log.debug('Done')

        self.use_fp16 = use_fp16

        self.log.debug(f'Use CPU: {use_cpu}')

        if not use_cpu:
            self.model = self.model.to('cuda')

    def transcribe(
            self,
            audio_bytes: bytes,
            temperature: float | Tuple[float, ...] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            beam_size: Optional[int] = None,
            patience: Optional[float] = None,
            best_of: Optional[int] = None,
    ) -> Transcribed:
        self.log.debug(
            f'Transcribing audio:\n'
            f'Audio size: {len(audio_bytes)} bytes\n'
            f'Temperature: {temperature}\n'
            f'Beam size: {beam_size}\n'
            f'Patience: {patience}\n'
            f'Best of: {best_of}'
        )

        audio = load_audio(audio_bytes)

        options_use_fp16 = False if self.model.device == 'cpu' else self.use_fp16

        start_transcribing_time = time.time()

        result = self.model.transcribe(
            audio=audio,
            temperature=temperature,
            beam_size=beam_size,
            patience=patience,
            fp16=options_use_fp16,
            best_of=best_of,
        )

        end_transcribing_time = time.time()

        res = Transcribed(
            language=result['language'],
            text=result['text'],
        )

        self.log.debug(
            f'Audio transcribed in {end_transcribing_time - start_transcribing_time:.3} seconds:\n'
            f'Language: {res.language}\n'
            f'Text: {res.text}'
        )

        return res
