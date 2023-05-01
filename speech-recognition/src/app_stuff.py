import logging
import os
import sys
from enum import Enum
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from common.result_cache import ResultCacheAbstract, DeclarativeBase
from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract


class ModelType(str, Enum):
    STUB: str = 'stub'
    WHISPER: str = 'whisper'


class ProgramArguments(BaseModel):
    model_path: str = Field(min_length=1)
    model_type: ModelType = Field(ModelType)
    device_override: Optional[str] = Field(None)
    use_fp16: bool = Field(False)
    log_level: str = Field('INFO', min_length=1)
    # Maximum elements in "result" cache. The "result" will go into cache after it was received.
    max_responses_in_cache: int = Field(100)
    # Maximum time in seconds "result" will be available after receiving it
    response_ttl: float = Field(60.0 * 30.0)
    # Use a cache for computed tasks. Hash will be used to determine whether result was already processed or not
    use_result_cache: bool = Field(True)
    result_cache_db_url: str = Field(None)


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model_path=os.environ.get('SERVER_MODEL_NAME_OR_PATH'),
        model_type=ModelType(os.environ.get('SERVER_MODEL_TYPE', ModelType.STUB)),
        device_override=os.environ.get('SERVER_DEVICE_OVERRIDE', None),
        use_fp16=os.environ.get('SERVER_USE_FP16', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        log_level=os.environ.get('SERVER_LOG_LEVEL', 'INFO'),
        max_responses_in_cache=int(os.environ.get('SERVER_MAX_RESPONSES_IN_CACHE', '100')),
        response_ttl=float(os.environ.get('SERVER_RESPONSE_TTL', '1800.0')),
        use_result_cache=os.environ.get('SERVER_USE_RESULT_CACHE', 'TRUE') in {'TRUE', 'true', '1', 'True'},
        result_cache_db_url=os.environ.get('SERVER_RESULT_CACHE_DB_URL', 'sqlite:///cache.sqlite3')
    )


def setup_and_get_logger(config_path: str, log_level: str):
    # Configure logging
    with open(config_path) as fp:
        conf = yaml.load(fp, Loader=yaml.FullLoader)

    conf['root']['level'] = log_level

    logging.config.dictConfig(conf)

    return logging.getLogger(f'{__name__}.main')


def get_result_cache(use_cache: bool, db_url: str) -> ResultCacheAbstract:
    if use_cache:
        from common.result_cache import ResultCache
        from sqlalchemy.future import Engine
        from sqlalchemy.future import create_engine
        from sqlalchemy.future import Connection

        engine: Engine = create_engine(db_url)
        with engine.begin() as conn:
            conn: Connection
            DeclarativeBase.metadata.create_all(bind=conn)

        return ResultCache(engine=engine)
    else:
        from common.result_cache import ResultCacheStub
        return ResultCacheStub()


def get_neural_network_or_exit_on_error(model_type: ModelType, model_path: str,
                                        device_override: str) -> CaptioningNeuralNetworkAbstract:
    if model_type == ModelType.STUB:
        from network.captioning_neural_network_stub import CaptioningNeuralNetworkStub

        return CaptioningNeuralNetworkStub()
    elif model_type == ModelType.WHISPER:
        from network.whisper_neural_network import WhisperNeuralNetwork

        return WhisperNeuralNetwork(path=model_path,
                                    device_override=device_override)
    else:
        print(f"Unknown model type: {model_type}", file=sys.stderr)
        sys.exit(-1)
