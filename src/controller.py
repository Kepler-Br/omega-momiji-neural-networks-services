import logging

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from starlette import status

from dto import GenerateMessageRequest, GenerateTextErrorResponse, \
    GenerateTextRequest
from generation_service import GenerationService


class Controller:
    def __init__(self,
                 generation_service: GenerationService
                 ):
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self._generation_service = generation_service
        self.router = APIRouter()

        self.router.add_api_route('/v1/completions', self.generate_text, methods=['POST'])
        self.router.add_api_route('/v1/chat/completions', self.generate_message, methods=['POST'])

    async def generate_message(self, request: GenerateMessageRequest) -> Response:
        try:
            response = await self._generation_service.generate_messages(request)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    response
                )
            )
        except RuntimeError as e:
            self._log.error('Error while trying to send message with parameters:\n'
                            f'{request.model_dump_json()}')
            self._log.error(e, exc_info=True)

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(
                    GenerateTextErrorResponse(
                        error_message=f'{str(e)}',
                        error_code='UNKNOWN_ERROR'
                    )
                )
            )
        except Exception as e:
            self._log.error('Unrecoverable exception while trying to send message')
            self._log.error(e, exc_info=True)
            raise e

    async def generate_text(self, request: GenerateTextRequest) -> Response:
        try:
            response = await self._generation_service.generate_text(request)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    response
                )
            )
        except RuntimeError as e:
            self._log.error('Error while trying to send message with parameters:\n'
                            f'{request.model_dump_json()}')
            self._log.error(e, exc_info=True)

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(
                    GenerateTextErrorResponse(
                        error_message=f'{str(e)}',
                        error_code='UNKNOWN_ERROR'
                    )
                )
            )
        except Exception as e:
            self._log.error('Unrecoverable exception while trying to send message')
            self._log.error(e, exc_info=True)
            raise e
