import logging
import os

import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field

from controller.controller import Controller
from network.image_captioning_abstract import ImageCaptioningAbstract
from network.image_captioning_stub import ImageCaptioningStub


class ProgramArguments(BaseModel):
    model: str = Field(min_length=1)
    use_stub: bool = Field(False)
    use_cpu: bool = Field(False)
    use_fp16: bool = Field(False)
    log_level: str = Field('INFO', min_length=1)


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model=os.environ.get('SERVER_MODEL_NAME_OR_PATH'),
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
neural_network: ImageCaptioningAbstract
if arguments.use_stub:
    neural_network = ImageCaptioningStub()
else:
    raise NotImplementedError('Non stub version is not implemented yet')

log.info('Done')

controller = Controller(network=neural_network)

app.include_router(controller.router)
