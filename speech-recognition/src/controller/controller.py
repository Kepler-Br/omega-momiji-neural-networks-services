import base64
import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from base_task_controller import BaseTaskController
from network.speech_recognition_abstract import SpeechRecognitionAbstract
from speech_recognize_request import SpeechRecognizeRequest
from speech_recognize_response import SpeechRecognizeResponse


class Controller(BaseTaskController):
    def __init__(
            self,
            network: SpeechRecognitionAbstract,
            max_cached_results: float,
            cached_result_ttl: float,
    ):
        super().__init__(
            task_executor=self._transcribe,
            logger=logging.getLogger(f'{__name__}.{self.__class__.__name__}'),
            max_cached_results=max_cached_results,
            cached_results_ttl=cached_result_ttl,
        )

        self._network = network

        self.router = APIRouter()

        self.router.add_api_route('/transcribed-audio/{task_key}', self.request_generation, methods=['PUT'])
        self.router.add_api_route('/transcribed-audio/{task_key}', self.get_result, methods=['GET'])

    def _transcribe(self, body: SpeechRecognizeRequest) -> SpeechRecognizeResponse:
        audio_bytes = base64.b64decode(body.audio)

        with self._network_lock:
            try:
                result = self._network.transcribe(
                    audio_bytes=audio_bytes,
                    temperature=body.temperature,
                    beam_size=body.beam_size,
                    patience=body.patience,
                    best_of=body.best_of,
                )

                return SpeechRecognizeResponse(
                    text=result.text,
                    language=result.language,
                )
            except RuntimeError as e:
                self.log.error(f'Error transcribing audio:')
                self.log.error(e, exc_info=True)

                return SpeechRecognizeResponse(
                    error_message=f'{e.__class__.__name__}: {e}',
                )

    def get_result(self, task_key: UUID) -> Response:
        return self._get_result(task_key=task_key)

    def request_generation(self, body: SpeechRecognizeRequest, task_key: UUID) -> Response:
        return self._request_task_execution(body=body, task_key=task_key)
