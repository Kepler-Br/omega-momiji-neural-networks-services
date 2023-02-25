import logging
import os
from typing import Optional

import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field

from controller.controller import Controller
from network.speech_recognition import SpeechRecognition
from network.speech_recognition_abstract import SpeechRecognitionAbstract
from network.speech_recognition_stub import SpeechRecognitionStub


class ProgramArguments(BaseModel):
    model: str = Field(min_length=1)
    model_dir: Optional[str] = Field(None)
    use_stub: bool = Field(False)
    use_cpu: bool = Field(False)
    use_fp16: bool = Field(False)
    log_level: str = Field('INFO', min_length=1)


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model=os.environ.get('SERVER_MODEL_NAME_OR_PATH'),
        model_dir=os.environ.get('SERVER_MODEL_SAVE_DIR'),
        use_stub=os.environ.get('SERVER_USE_STUB', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_fp16=os.environ.get('SERVER_USE_FP16', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_cpu=os.environ.get('SERVER_USE_CPU', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        log_level=os.environ.get('SERVER_LOG_LEVEL', 'INFO'),
    )


app = FastAPI()

arguments = parse_arguments()

# Configure logging
with open('logging.yaml') as fp:
    conf = yaml.load(fp, Loader=yaml.FullLoader)

conf['root']['level'] = arguments.log_level

logging.config.dictConfig(conf)

log = logging.getLogger(f'{__name__}.main')

# Loading stuff
log.info('Loading model')
neural_network: SpeechRecognitionAbstract
if arguments.use_stub:
    neural_network = SpeechRecognitionStub()
else:
    neural_network = SpeechRecognition(
        arguments.model,
        use_cpu=arguments.use_cpu,
        use_fp16=arguments.use_fp16,
        download_root=arguments.model_dir
    )

log.info('Done')

controller = Controller(network=neural_network)

app.include_router(controller.router)
