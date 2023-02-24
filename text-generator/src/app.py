import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from controller import Controller
from language_neural_network import LanguageNeuralNetwork
from language_neural_network_abstract import LanguageNeuralNetworkAbstract
from language_neural_network_stub import LanguageNeuralNetworkStub


class ProgramArguments(BaseModel):
    model: str = Field(min_length=1)
    use_stub: bool = Field(False)
    use_cpu: bool = Field(False)
    log_level: str = Field('INFO', min_length=1)


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model=os.environ.get('SERVER_MODEL_PATH'),
        use_stub=os.environ.get('SERVER_USE_STUB', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_cpu=os.environ.get('SERVER_USE_CPU', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        log_level=os.environ.get('SERVER_LOG_LEVEL', 'INFO'),
    )


app = FastAPI()

arguments = parse_arguments()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
)

log = logging.getLogger(__name__)
log.setLevel(arguments.log_level)

log.info('Loading GPT...')

neural_network: LanguageNeuralNetworkAbstract
if arguments.use_stub:
    neural_network = LanguageNeuralNetworkStub(arguments.model, use_cpu=arguments.use_cpu)
else:
    neural_network = LanguageNeuralNetwork(arguments.model, use_cpu=arguments.use_cpu)

log.info('Done')

controller = Controller(network=neural_network)

# Registering routes
app.include_router(controller.router)
