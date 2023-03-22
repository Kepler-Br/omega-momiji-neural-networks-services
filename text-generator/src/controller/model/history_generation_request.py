from typing import Optional

from pydantic import BaseModel, Field

from controller.model.message import Message


class GenerationParams(BaseModel):
    temperature: float = Field(1.0, ge=0.0)
    max_new_tokens: int = Field(20, gt=0)
    num_beams: int = Field(5, gt=0)
    repetition_penalty: float = Field(2.0, ge=1.0)
    early_stopping: bool = Field(True)
    seed: int = Field(42)
    top_k: int = Field(50, gt=0)
    top_p: float = Field(0.95, gt=0.0, le=1.0)
    no_repeat_ngram_size: Optional[int] = Field(1, ge=0)
    bad_words: Optional[list[str]] = Field(None)


class ControllerRequest(BaseModel):
    generation_params: GenerationParams = Field()
    message_type: str = Field()
    prompt: Optional[str] = Field(None)
    prompt_author: str = Field()
    reply_to_message_id: Optional[int] = Field(None)
    history: list[Message] = Field()
