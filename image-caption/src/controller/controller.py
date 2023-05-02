import base64
import logging
from uuid import UUID

from fastapi import APIRouter, Header, Path
from fastapi.responses import Response
from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract

from common.result_cache import ResultCacheAbstract
from .base_task_controller import BaseTaskController
from .model.requests import ControllerRequest
from .model.responses import CaptionResponse, ResponseStatus


class Controller(BaseTaskController):
    def __init__(
            self,
            network: CaptioningNeuralNetworkAbstract,
            max_cached_results: float,
            cached_result_ttl: float,
            result_cache: ResultCacheAbstract,
    ):
        super().__init__(
            task_executor=self._generate,
            logger=logging.getLogger(f'{__name__}.{self.__class__.__name__}'),
            max_cached_results=max_cached_results,
            cached_results_ttl=cached_result_ttl,
        )

        self._network = network

        self.router = APIRouter()

        self.router.add_api_route('/image-captions', self.request_task_execution, methods=['POST'])
        self.router.add_api_route('/image-captions/{task_key}', self.get_result, methods=['GET'])

        self.result_cache = result_cache

    def _generate(self, body: ControllerRequest) -> CaptionResponse:
        try:
            digest = self.result_cache.calc_digest(body.data, body.condition, self._network.name())
            cached = self.result_cache.get(digest)

            if cached is not None:
                self.log.info(f'Using cached result: "{cached}"')

                return CaptionResponse(
                    status=ResponseStatus.OK,
                    caption=cached
                )

            with self._network_lock:
                result = self._network.caption(
                    image=base64.b64decode(body.data),
                    condition=body.condition
                )

                self.result_cache.put(digest=digest, result=result)

                return CaptionResponse(
                    status=ResponseStatus.OK,
                    caption=result
                )
        except Exception as e:
            self.log.error('Error captioning image:', e, exc_info=True)

            return CaptionResponse(
                status=ResponseStatus.INTERNAL_SERVER_ERROR,
                error_message=f'{e.__class__.__name__}: {e}',
            )

    def get_result(self, task_key: UUID = Path(), run_async: bool | None = Header(False)) -> Response:
        return self._get_result_handling(task_key=task_key, run_async=run_async)

    def request_task_execution(self, body: ControllerRequest) -> Response:
        return self._request_task_execution_handling(body=body)
