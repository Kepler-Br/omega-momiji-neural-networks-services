import logging
import os
import sys
from enum import Enum
from typing import Optional

import pydantic
import yaml
from pydantic import BaseModel, Field

from common.result_cache import ResultCacheAbstract, DeclarativeBase
from network.captioning_neural_network_abstract import CaptioningNeuralNetworkAbstract


class ModelType(str, Enum):
    STUB: str = 'stub'
    BLIP: str = 'BLIP'
    BLIP2: str = 'BLIP2'
    CLIP_INTERROGATOR: str = 'CLIP_INTERROGATOR'


class ClipInterrogatorArguments(BaseModel):
    clip_model_name: str = Field(alias='SERVER_CLIP_INTERROGATOR_MODEL_NAME')
    chunk_size: int = Field(alias='SERVER_CLIP_INTERROGATOR_CHUNK_SIZE')
    caption_model_name: str = Field(alias='SERVER_CLIP_INTERROGATOR_CAPTION_MODEL_NAME')
    caption_max_length: int = Field(alias='SERVER_CLIP_INTERROGATOR_MAX_LENGTH')

    class Config:
        allow_population_by_field_name = True


class ProgramArguments(BaseModel):
    model_path: str = Field(min_length=1, alias='SERVER_MODEL_NAME_OR_PATH')
    model_type: ModelType = Field(ModelType, alias='SERVER_MODEL_TYPE')
    device_override: Optional[str] = Field(None, alias='SERVER_DEVICE_OVERRIDE')
    use_fp16: bool = Field(False, alias='SERVER_USE_FP16')
    log_level: str = Field('INFO', min_length=1, alias='SERVER_LOG_LEVEL')
    # Maximum elements in "result" cache. The "result" will go into cache after it was received.
    max_responses_in_cache: int = Field(100, alias='SERVER_MAX_RESPONSES_IN_CACHE')
    # Maximum time in seconds "result" will be available after receiving it
    response_ttl: float = Field(60.0 * 30.0, alias='SERVER_RESPONSE_TTL')
    # Use a cache for computed tasks. Hash will be used to determine whether result was already processed or not
    use_result_cache: bool = Field(True, alias='SERVER_USE_RESULT_CACHE')
    result_cache_db_url: str = Field(None, alias='SERVER_RESULT_CACHE_DB_URL')
    clip_interrogator_arguments: ClipInterrogatorArguments = Field(None)

    class Config:
        allow_population_by_field_name = True


def parse_arguments() -> ProgramArguments:
    try:
        arguments = ProgramArguments(
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

        if arguments.model_type == ModelType.CLIP_INTERROGATOR:
            arguments.clip_interrogator_arguments = ClipInterrogatorArguments(
                clip_model_name=os.environ.get('SERVER_CLIP_INTERROGATOR_MODEL_NAME'),
                chunk_size=int(os.environ.get('SERVER_CLIP_INTERROGATOR_CHUNK_SIZE', '2048')),
                caption_model_name=os.environ.get('SERVER_CLIP_INTERROGATOR_CAPTION_MODEL_NAME', 'blip-large'),
                caption_max_length=int(os.environ.get('SERVER_CLIP_INTERROGATOR_MAX_LENGTH', '32')),
            )

        return arguments
    except pydantic.error_wrappers.ValidationError as e:
        print(e)
        sys.exit(-1)


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


def get_neural_network_or_exit_on_error(arguments: ProgramArguments) -> CaptioningNeuralNetworkAbstract:
    if arguments.model_type == ModelType.STUB:
        from network.captioning_neural_network_stub import CaptioningNeuralNetworkStub

        return CaptioningNeuralNetworkStub()
    elif arguments.model_type == ModelType.BLIP:
        from network.blip_captioning_neural_network import BlipCaptioningNeuralNetwork

        return BlipCaptioningNeuralNetwork(path=arguments.model_path,
                                           device_override=arguments.device_override)
    elif arguments.model_type == ModelType.BLIP2:
        from network.blip2_captioning_neural_network import Blip2CaptioningNeuralNetwork

        return Blip2CaptioningNeuralNetwork(path=arguments.model_path,
                                            device_override=arguments.device_override)
    elif arguments.model_type == ModelType.CLIP_INTERROGATOR:
        from network.clip_interrogator_neural_network import ClipInterrogatorNeuralNetwork

        clip_arguments = arguments.clip_interrogator_arguments

        return ClipInterrogatorNeuralNetwork(clip_name=clip_arguments.clip_model_name,
                                             caption_name=clip_arguments.caption_model_name,
                                             chunk_size=clip_arguments.chunk_size,
                                             caption_max_length=clip_arguments.caption_max_length,
                                             device_override=arguments.device_override)
    else:
        print(f"Unknown model type: {arguments.model_type}", file=sys.stderr)
        sys.exit(-1)
