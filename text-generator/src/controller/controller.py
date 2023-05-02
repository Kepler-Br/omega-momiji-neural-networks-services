import logging
from uuid import UUID

from fastapi import APIRouter, Header, Path
from starlette.responses import JSONResponse

from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract
from .base_task_controller import BaseTaskController
from .model.history_generation_request import ControllerRequest
from .model.responses import HistoryGenerationResponse, ResponseStatus


class Controller(BaseTaskController):
    def __init__(
            self,
            network: LanguageNeuralNetworkAbstract,
            max_cached_responses: float,
            cached_responses_ttl: float,
    ):
        super().__init__(
            task_executor=self._generate,
            logger=logging.getLogger(f'{__name__}.{self.__class__.__name__}'),
            max_cached_results=max_cached_responses,
            cached_results_ttl=cached_responses_ttl,
        )

        self._network = network

        self.router = APIRouter()

        self.router.add_api_route('/history-prompts', self.request_task_execution, methods=['POST'])
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

                return HistoryGenerationResponse(
                    status=ResponseStatus.OK,
                    messages=result
                )
        except Exception as e:
            self.log.error('Error generating text:', e, exc_info=True)

            return HistoryGenerationResponse(
                status=ResponseStatus.INTERNAL_SERVER_ERROR,
                error_message=f'{e.__class__.__name__}: {e}',
            )

    def get_result(self, task_key: UUID = Path(), run_async: bool | None = Header(False)) -> JSONResponse:
        return self._get_result_handling(task_key=task_key, run_async=run_async)

    def request_task_execution(self, body: ControllerRequest) -> JSONResponse:
        return self._request_task_execution_handling(body=body)
