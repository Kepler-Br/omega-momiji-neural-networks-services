import base64
import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from controller.base_task_controller import BaseTaskController
from controller.controller_request import ControllerRequest
from controller.controller_response import ControllerResponse
from network.image_captioning_abstract import ImageCaptioningAbstract


class Controller(BaseTaskController):
    def __init__(self, network: ImageCaptioningAbstract):
        super().__init__(
            self._caption,
            logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        )

        self.network = network

        self.router = APIRouter()

        self.router.add_api_route('/captioned-image/{task_key}', self.request_task_execution, methods=['POST'])
        self.router.add_api_route('/captioned-image/{task_key}', self.get_result, methods=['GET'])

    def _caption(self, body: ControllerRequest) -> ControllerResponse:
        image_bytes = base64.b64decode(body.image)

        with self.network_lock:
            try:
                result = self.network.caption(
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
