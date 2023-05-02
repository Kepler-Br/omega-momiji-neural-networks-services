import logging
import os
import sys
from enum import Enum
from typing import Optional

import pydantic
import yaml
from pydantic import BaseModel, Field

from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract


class ModelType(str, Enum):
    STUB: str = 'stub'
    GPT2: str = 'GPT2'


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

    class Config:
        allow_population_by_field_name = True


def parse_arguments() -> ProgramArguments:
    try:
        return ProgramArguments(
            model_path=os.environ.get('SERVER_MODEL_NAME_OR_PATH'),
            model_type=ModelType(os.environ.get('SERVER_MODEL_TYPE', ModelType.STUB)),
            device_override=os.environ.get('SERVER_DEVICE_OVERRIDE', None),
            use_fp16=os.environ.get('SERVER_USE_FP16', 'FALSE') in {'TRUE', 'true', '1', 'True'},
            log_level=os.environ.get('SERVER_LOG_LEVEL', 'INFO'),
            max_responses_in_cache=int(os.environ.get('SERVER_MAX_RESPONSES_IN_CACHE', '100')),
            response_ttl=float(os.environ.get('SERVER_RESPONSE_TTL', '1800.0')),
        )
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


def get_neural_network_or_exit_on_error(model_type: ModelType, model_path: str,
                                        device_override: str) -> LanguageNeuralNetworkAbstract:
    if model_type == ModelType.STUB:
        from network.language_neural_network_stub import LanguageNeuralNetworkStub

        return LanguageNeuralNetworkStub()
    elif model_type == ModelType.GPT2:
        from network.gpt2_neural_network import GPT2NeuralNetwork

        return GPT2NeuralNetwork(path=model_path,
                                 device_override=device_override)
    else:
        print(f"Unknown model type: {model_type}", file=sys.stderr)
        sys.exit(-1)
