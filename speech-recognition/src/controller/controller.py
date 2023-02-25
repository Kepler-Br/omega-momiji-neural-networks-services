import base64
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from starlette import status

from controller.speech_recognize_request import SpeechRecognizeRequest
from controller.speech_recognize_response import SpeechRecognizeResponse
from network.speech_recognition_abstract import SpeechRecognitionAbstract
from network.transcribed import Transcribed


class Controller:
    def __init__(self, network: SpeechRecognitionAbstract):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self._network = network
        self._network_lock = threading.RLock()
        self._tasks_lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._tasks: dict[UUID, Future[Transcribed]] = dict()

        self.router = APIRouter()

        self.router.add_api_route('/transcribed-audio/{task_key}', self.request_generation, methods=['POST'])
        self.router.add_api_route('/transcribed-audio/{task_key}', self.get_generation, methods=['GET'])

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

    def get_generation(self, task_key: UUID) -> Response:
        if task_key not in self._tasks:
            self.log.debug(f'Requested not existing task: {task_key}')
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        task = self._tasks[task_key]

        if not task.done():
            self.log.debug(f'Requested task that is not ready: {task_key}')
            return Response(status_code=status.HTTP_425_TOO_EARLY)

        result = task.result()

        self._tasks.pop(task_key)

        self.log.debug(f'Task received: {task_key}')

        return JSONResponse(
            content=result.dict(exclude_none=True)
        )

    def request_generation(self, body: SpeechRecognizeRequest, task_key: UUID) -> Response:
        if task_key not in self._tasks:
            self.log.info(f'Submitted task {task_key}')
            self._tasks[task_key] = self._executor.submit(self._transcribe, body)
        else:
            self.log.info(f'Task already exists: {task_key}')

        return Response(
            status_code=status.HTTP_201_CREATED
        )
