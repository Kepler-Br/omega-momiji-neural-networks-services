from enum import Enum

import yaml
from pydantic import Field, BaseModel

import logging
import logging.config

from tools import get_dict_key_by_path

class PromptTemplateType(str, Enum):
    MISTRAL_V3 = 'MistralV3'


class NeuralNetworkConfig(BaseModel):
    backend: str = Field()
    temperature: float = Field(ge=0.0)
    prompt_template: PromptTemplateType = Field()
    context: int = Field(ge=1)
    mock: bool = Field()


class AppConfig(BaseModel):
    neural_network: NeuralNetworkConfig = Field()


def load_logging_config(config_file: str):
    """Load logging configuration from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    except FileNotFoundError as e:
        print(f"Logging config file '{config_file}' not found.")
        raise e
    except yaml.YAMLError as e:
        print(f"Failed to parse YAML in logging config: {e}")
        raise e
    except Exception as e:
        print(f"Error loading logging config: {e}")
        raise e


def load_config(config_file: str) -> AppConfig:
    """Load configuration from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f.read())
            return AppConfig(
                neural_network=NeuralNetworkConfig(
                    backend=get_dict_key_by_path(config, 'neural-network.backend'),
                    temperature=get_dict_key_by_path(config, 'neural-network.temperature'),
                    prompt_template=get_dict_key_by_path(config, 'neural-network.prompt-template'),
                    context=get_dict_key_by_path(config, 'neural-network.context'),
                    mock=get_dict_key_by_path(config, 'neural-network.mock'),
                )
            )
    except FileNotFoundError as e:
        print(f"Config file '{config_file}' not found.")
        raise e
    except yaml.YAMLError as e:
        print(f"Failed to parse YAML in config: {e}")
        raise e
    except Exception as e:
        print(f"Error loading config: {e}")
        raise e
