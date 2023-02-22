import os
import threading

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from generate import LanguageNeuralNetwork


class GenerateTextRequest(BaseModel):
    prompt: str = Field(min_length=1)
    temperature: float = Field(ge=0.0)
    repetition_penalty: float = Field(None, ge=1.0)
    count: int = Field(1, ge=0)
    max_new_tokens: int = Field(20, gt=0)
    num_beams: int = Field(5, gt=0)
    top_k: int = Field(50, gt=0)
    top_p: float = Field(0.95, gt=0.0, le=1.0)
    no_repeat_ngram_size: int = Field(1, ge=0)
    early_stopping: bool = Field(True)
    seed: int = Field(42)
    bad_words: list[str] = Field(None)


class GeneratedResponse(BaseModel):
    text: list[str]


model_path = os.environ['MODEL']
use_cpu = bool(os.environ.get('USE_CPU', 0))

print(f'Using CPU: {use_cpu}')

neural_network = LanguageNeuralNetwork(model_path, use_cpu=use_cpu)
app = FastAPI()

lock = threading.RLock()


@app.post('/generated-text')
def generate_text(body: GenerateTextRequest) -> GeneratedResponse:
    with lock:
        generated: list[str] = neural_network.generate(
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

    return GeneratedResponse(text=generated)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=4557, reload=False, workers=1)
