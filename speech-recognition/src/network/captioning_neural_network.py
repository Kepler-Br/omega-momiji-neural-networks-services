import logging

import ffmpeg
import numpy as np
import whisper

from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract


class CaptioningNeuralNetwork(CaptioningNeuralNetworkAbstract):
    def __init__(self, path: str, use_cpu: bool = False):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self.use_cpu = use_cpu
        self.log.debug('Loading model')

        self.model = whisper.load_model(
            name=path,
            device='cpu' if self.use_cpu else 'cuda'
        )

        self.log.debug('Done')

    @staticmethod
    def _load_audio(audio_bytes: bytes, sr: int = 16000) -> np.ndarray:
        # Slightly modified code by this author:
        # https://github.com/openai/whisper/discussions/380#discussioncomment-3928648
        """
        Open an audio file and read as mono waveform, resampling as necessary

        Parameters
        ----------
        audio_bytes: bytes
            Bytes of audio file

        sr: int
            The sample rate to resample the audio if necessary

        Returns
        -------
        A NumPy array containing the audio waveform, in float32 dtype.
        """

        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input('pipe:', threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=audio_bytes)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    def caption(
            self,
            voice: bytes,
    ) -> str:
        audio = self._load_audio(voice)

        return self.model.transcribe(audio)['text']