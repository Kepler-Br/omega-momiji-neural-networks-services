import base64
import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from base_task_controller import BaseTaskController
from controller_request import ControllerRequest
from controller_response import ControllerResponse
from network.image_captioning_abstract import ImageCaptioningAbstract


class Controller(BaseTaskController):
    def __init__(
            self,
            network: ImageCaptioningAbstract,
            max_cached_results: float,
            cached_result_ttl: float,
    ):
        super().__init__(
            task_executor=self._caption,
            logger=logging.getLogger(f'{__name__}.{self.__class__.__name__}'),
            max_cached_results=max_cached_results,
            cached_results_ttl=cached_result_ttl,
        )

        self._network = network

        self.router = APIRouter()

        self.router.add_api_route('/captioned-image/{task_key}', self.request_task_execution, methods=['PUT'])
        self.router.add_api_route('/captioned-image/{task_key}', self.get_result, methods=['GET'])

    def _caption(self, body: ControllerRequest) -> ControllerResponse:
        image_bytes = base64.b64decode(body.image)

        with self._network_lock:
            try:
                result = self._network.caption(
                    image_bytes=image_bytes,
                )

                return ControllerResponse(
                    text=result.text
                )
            except RuntimeError as e:
                self.log.error(f'Error captioning image:')
                self.log.error(e, exc_info=True)

                return ControllerResponse(
                    error_message=f'{e.__class__.__name__}: {e}',
                )

    def get_result(self, task_key: UUID) -> Response:
        return self._get_result(task_key=task_key)

    def request_task_execution(self, body: ControllerRequest, task_key: UUID) -> Response:
        return self._request_task_execution(body=body, task_key=task_key)
