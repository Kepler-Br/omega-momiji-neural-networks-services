from abc import abstractmethod, ABC
from typing import List, final
from weakref import finalize

import aiohttp
from pydantic import BaseModel, Field
from urllib.parse import urljoin


class GenerationInput(BaseModel):
    max_context_length: int = Field()
    max_length: int = Field()
    prompt: str = Field()
    stop_sequence: List[str] = Field()
    temperature: float = Field()
    rep_pen: float = Field()
    top_k: int = Field()
    top_p: float = Field()


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
                       repetition_penalty: float,
                       top_p: float,
                       top_k: int,
                       ) -> GenerationOutput:
        pass


class MockKoboldClient(KoboldClient):
    async def generate(self,
                       max_context_length: int,
                       max_length: int,
                       prompt: str,
                       stop_sequence: List[str],
                       temperature: float,
                       repetition_penalty: float,
                       top_p: float,
                       top_k: int,
                       ) -> GenerationOutput:
        return GenerationOutput(
            results=[
                GenerationResult(
                    text='This is a mock',
                    finish_reason='length'
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
                       repetition_penalty: float,
                       top_p: float,
                       top_k: int,
                       ) -> GenerationOutput:
        async with aiohttp.ClientSession() as session:
            request_body = GenerationInput(
                max_context_length=max_context_length,
                max_length=max_length,
                prompt=prompt,
                stop_sequence=stop_sequence,
                temperature=temperature,
                rep_pen=repetition_penalty,
                top_k=top_k,
                top_p=top_p,
            )
            url = urljoin(self._url, 'api/v1/generate')

            async with session.post(url, json=request_body.model_dump()) as response:
                resp = await response.json()
                return GenerationOutput(**resp)
