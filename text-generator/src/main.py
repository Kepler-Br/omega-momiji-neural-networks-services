import logging
import os
from dataclasses import dataclass

from fastapi import FastAPI

from controller import Controller
from language_neural_network import LanguageNeuralNetwork
from language_neural_network_abstract import LanguageNeuralNetworkAbstract
from language_neural_network_stub import LanguageNeuralNetworkStub


@dataclass
class ProgramArguments:
    model: str
    use_stub: bool
    use_cpu: bool
    port: int
    host: str
    workers: int
    log_level: str


def parse_arguments() -> ProgramArguments:
    return ProgramArguments(
        model=os.environ.get('SERVER_MODEL_PATH'),
        use_stub=os.environ.get('SERVER_USE_STUB', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        use_cpu=os.environ.get('SERVER_USE_CPU', 'FALSE') in {'TRUE', 'true', '1', 'True'},
        port=int(os.environ.get('SERVER_PORT', '8080')),
        host=os.environ.get('SERVER_HOST', '0.0.0.0'),
        workers=int(os.environ.get('SERVER_WORKERS', '2')),
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
