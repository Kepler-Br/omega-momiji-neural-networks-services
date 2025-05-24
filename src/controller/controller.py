import logging
from typing import Optional, List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from pyrogram import Client as PyrogramClient, enums
from starlette import status


class GenerateTextRequest(BaseModel):
    text: str = Field()
    max_context_length: int = Field()
    max_length: int = Field()

class GenerateTextErrorResponse(BaseModel):
    error_message: str = Field()
    error_code: str = Field()

class GenerateTextResponse(BaseModel):
    text: str = Field()

class Message(BaseModel):
    id: str = Field()
    text: Optional[str] = Field()
    media_type: Optional[str] = Field()
    media_caption: Optional[str] = Field()
    reply_to: str = Field()


class Controller:
    def __init__(self,
                 pyrogram_client: PyrogramClient
                 ):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.pyrogram_client = pyrogram_client
        self.router = APIRouter()

        self.router.add_api_route('/v1/completions', self.generate_text, methods=['POST'])
        self.router.add_api_route('/v1/chat/completions', self.generate_message, methods=['POST'])

    async def generate_message(self, request) -> Response:
        try:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    GenerateTextResponse(
                        text="123321"
                    )
                )
            )
        except RuntimeError as e:
            self.log.error('Error while trying to send message with parameters:\n'
                           f'{request.model_dump_json()}')
            self.log.error(e, exc_info=True)

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
            self.log.error('Unrecoverable exception while trying to send message')
            self.log.error(e, exc_info=True)
            raise e


    async def generate_text(self, request: GenerateTextRequest) -> Response:
        try:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    GenerateTextResponse(
                        text="123321"
                    )
                )
            )
        except RuntimeError as e:
            self.log.error('Error while trying to send message with parameters:\n'
                           f'{request.model_dump_json()}')
            self.log.error(e, exc_info=True)

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
            self.log.error('Unrecoverable exception while trying to send message')
            self.log.error(e, exc_info=True)
            raise e
