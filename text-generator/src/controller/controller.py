import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from starlette import status

from base_task_controller import BaseTaskController
from controller_request import ControllerRequest
from controller_response import ControllerResponse
from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract


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

        self.router.add_api_route('/generated-text/{task_key}', self.request_task_execution, methods=['PUT'])
        self.router.add_api_route('/generated-text/{task_key}', self.get_result, methods=['GET'])

    def _generate(self, body: ControllerRequest) -> ControllerResponse:
        try:
            with self._network_lock:
                result = self._network.generate(
                    prompt=body.prompt,
                    count=body.count,
                    max_new_tokens=body.max_new_tokens,
                    num_beams=body.num_beams,
                    no_repeat_ngram_size=body.no_repeat_ngram_size,
                    early_stopping=body.early_stopping,
                    seed=body.seed,
                    bad_words=body.bad_words,
                    top_k=body.top_k,
                    top_p=body.top_p,
                    temperature=body.temperature,
                    repetition_penalty=body.repetition_penalty,
                )

                return ControllerResponse(
                    text=result,
                )
        except RuntimeError as e:
            self.log.error(f'Error generating text:')
            self.log.error(e, exc_info=True)

            return ControllerResponse(
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
