import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from base_task_controller import BaseTaskController
from controller_request import ControllerRequest
from controller_response import ControllerResponse
from network.image_generator_abstract import ImageGeneratorAbstract


class Controller(BaseTaskController):
    def __init__(
            self,
            network: ImageGeneratorAbstract,
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

        self.router.add_api_route('/generated-image/{task_key}', self.request_task_execution, methods=['PUT'])
        self.router.add_api_route('/generated-image/{task_key}', self.get_result, methods=['GET'])

    def _generate(self, body: ControllerRequest) -> ControllerResponse:
        with self._network_lock:
            try:
                result = self._network.generate_image(
                    prompt=body.prompt,
                    negative_prompt=body.negative_prompt,
                )

                return ControllerResponse(
                    image=result.image
                )
            except RuntimeError as e:
                self.log.error(f'Error generating image with parameters:\n'
                               f'Prompt: {body.prompt}',
                               f'Negative prompt: {body.negative_prompt}',
                               )
                self.log.error(e, exc_info=True)

                return ControllerResponse(
                    error_message=f'{e.__class__.__name__}: {e}',
                )

    def get_result(self, task_key: UUID) -> Response:
        return self._get_result(task_key=task_key)

    def request_task_execution(self, body: ControllerRequest, task_key: UUID) -> Response:
        return self._request_task_execution(body=body, task_key=task_key)
