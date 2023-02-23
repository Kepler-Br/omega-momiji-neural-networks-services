from pydantic import BaseModel, Field


class GenerateTextRequest(BaseModel):
    prompt: str = Field(min_length=1)
    temperature: float = Field(1.0, ge=0.0)
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
