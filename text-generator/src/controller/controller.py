import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from starlette import status

from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract
from .base_task_controller import BaseTaskController
from .model.history_generation_request import ControllerRequest
from .model.responses import HistoryGenerationResponse


class Controller(BaseTaskController):
    def __init__(
            self,
            network: LanguageNeuralNetworkAbstract,
            max_cached_results: float,
            cached_result_ttl: float,
    ):
        super().__init__(
            task_executor=self._generate,
            logger=logging.getLogger(f'{__name__}.{self.__class__.__name__}'),
            max_cached_results=max_cached_results,
            cached_results_ttl=cached_result_ttl,
        )

        self._network = network

        self.router = APIRouter()

        self.router.add_api_route('/history-prompts/{task_key}', self.request_task_execution, methods=['PUT'])
        self.router.add_api_route('/history-prompts/{task_key}', self.get_result, methods=['GET'])

    def _generate(self, body: ControllerRequest) -> HistoryGenerationResponse:
        try:
            with self._network_lock:
                generation_params = body.generation_params

                result = self._network.generate_messages(
                    messages=body.history,
                    generation_params=generation_params,
                    prompt_author=body.prompt_author,
                    reply_to_id=body.reply_to_message_id,
                    prompt=body.prompt,
                )

                return ControllerResponse(
                    status=ResponseStatus.OK,
                    messages=result
                )
        except RuntimeError as e:
            self.log.error('Error generating text:')
            self.log.error(e, exc_info=True)

            return ControllerResponse(
                status=ResponseStatus.INTERNAL_SERVER_ERROR,
                error_message=f'{e.__class__.__name__}: {e}',
            )

    def get_generation(self, task_key: UUID) -> Response:
        if task_key not in self._tasks:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        task = self._tasks[task_key]

        if not task.done():
            return Response(status_code=status.HTTP_425_TOO_EARLY)

        result = task.result()

        self._tasks.pop(task_key)

        return JSONResponse(
            content=result.dict(exclude_none=True)
        )

    def get_result(self, task_key: UUID) -> Response:
        return self._get_result(task_key=task_key)

    def request_task_execution(self, body: ControllerRequest, task_key: UUID) -> Response:
        return self._request_task_execution(body=body, task_key=task_key)
