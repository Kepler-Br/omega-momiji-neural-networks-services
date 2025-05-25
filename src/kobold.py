from abc import abstractmethod, ABC
from typing import List

import aiohttp
from pydantic import BaseModel, Field
from urllib.parse import urljoin


class GenerationInput(BaseModel):
    max_context_length: int = Field()
    max_length: int = Field()
    prompt: str = Field()
    stop_sequence: List[str] = Field()
    temperature: float = Field()


class GenerationResult(BaseModel):
    text: str = Field()
    finish_reason: str = Field()


class GenerationOutput(BaseModel):
    results: List[GenerationResult] = Field(min_length=1)


class KoboldClient(ABC):
    @abstractmethod
    async def generate(self,
                       max_context_length: int,
                       max_length: int,
                       prompt: str,
                       stop_sequence: List[str],
                       temperature: float,
                       ) -> GenerationOutput:
        pass


class MockKoboldClient(KoboldClient):
    async def generate(self,
                       max_context_length: int,
                       max_length: int,
                       prompt: str,
                       stop_sequence: List[str],
                       temperature: float,
                       ) -> GenerationOutput:
        return GenerationOutput(
            results=[
                GenerationResult(
                    text='This is a mock'
                )
            ]
        )


class AsyncKoboldClient(KoboldClient):
    def __init__(self, url: str):
        assert url is not None

        self._url: str = url

    async def generate(self,
                       max_context_length: int,
                       max_length: int,
                       prompt: str,
                       stop_sequence: List[str],
                       temperature: float,
                       ) -> GenerationOutput:
        async with aiohttp.ClientSession() as session:
            request_body = GenerationInput(
                max_context_length=max_context_length,
                max_length=max_length,
                prompt=prompt,
                stop_sequence=stop_sequence,
                temperature=temperature,
            )
            url = urljoin(self._url, 'api/v1/generate')

            async with session.post(url, json=request_body.model_dump()) as response:
                resp = await response.json()
                return GenerationOutput(**resp)
