import logging
import os

import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field

from controller.controller import Controller
from network.image_generator_abstract import ImageGeneratorAbstract
from network.image_generator_stub import ImageGeneratorStub


class ProgramArguments(BaseModel):
    model: str = Field(min_length=1)
    use_stub: bool = Field(False)
    use_cpu: bool = Field(False)
    use_fp16: bool = Field(False)
    log_level: str = Field('INFO', min_length=1)
    # Maximum elements in "result" cache. The "result" will go into cache after it was received.
    max_results_in_cache: int = Field(100)
    # Maximum time in seconds "result" will be available after receiving it
    result_ttl: float = Field(60.0 * 30.0)


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model=os.environ.get('SERVER_MODEL_NAME_OR_PATH'),
        use_stub=os.environ.get('SERVER_USE_STUB', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_fp16=os.environ.get('SERVER_USE_FP16', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_cpu=os.environ.get('SERVER_USE_CPU', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        log_level=os.environ.get('SERVER_LOG_LEVEL', 'INFO'),
        max_results_in_cache=int(os.environ.get('SERVER_MAX_RESULTS_IN_CACHE')),
        result_ttl=float(os.environ.get('SERVER_RESULT_TTL')),
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
neural_network: ImageGeneratorAbstract
if arguments.use_stub:
    neural_network = ImageGeneratorStub()
else:
    raise NotImplementedError('Non stub version is not implemented yet')

log.info('Done')

controller = Controller(
    network=neural_network,
    max_cached_results=arguments.max_results_in_cache,
    cached_result_ttl=arguments.result_ttl,
)

app.include_router(controller.router)
