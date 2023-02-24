### Text generator

#### How to run

```shell
uvicorn app:app --host='0.0.0.0' --port='8080' --workers=2
```

#### A list of environment variables used by program

| Key               | Required | Type    | Possible values                               | Default |
|-------------------|----------|---------|-----------------------------------------------|---------|
| SERVER_MODEL_PATH | Yes      | String  | File system or hugging face path              |         |
| SERVER_USE_STUB   | No       | Boolean | TRUE, true, 1, True, **Any string as False**  | False   |
| SERVER_USE_CPU    | No       | Boolean | TRUE, true, 1, True, **Any string as False**  | False   |
| SERVER_LOG_LEVEL  | No       | String  | NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO    |

#### A list of environment variables used by run.py

| Key            | Required | Type    | Possible values     | Default |
|----------------|----------|---------|---------------------|---------|
| SERVER_PORT    | No       | Integer | A valid port number | 8080    |
| SERVER_HOST    | No       | String  | A valid IP address  | 0.0.0.0 |
| SERVER_WORKERS | No       | Integer | 1>                  | 2       |

#### Request

```python
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
```

Example

```json
{
    "prompt": "---- 10000031\n-- User\n234\n---- 10000030\n-- User\n",
    "count": 1,
    "max_new_tokens": 30,
    "bad_words": ["[STICKER]","[PHOTO]"],
    "seed": 1234580
}
```

#### Response

```python
class GeneratedResponse(BaseModel):
    text: list[str]
```

Example

```json
{
    "result": [
        "some generated text"
    ]
}
```
