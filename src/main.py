import logging.config
import yaml
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from config import load_logging_config, load_config, PromptTemplateType
from controller import Controller
from generation_service import GenerationService
from kobold import MockKoboldClient, AsyncKoboldClient
from text_wrapper import MistralV7TextPrompt

# Load the logging configuration
load_logging_config('logging.yaml')
config = load_config('config.yaml')

# Get the root logger
logger = logging.getLogger(__name__)

app = FastAPI()


def get_openapi():
    with open("static/text-generation-contract.yaml", "r") as openapi:
        return yaml.load(openapi, Loader=yaml.FullLoader)


app.openapi = get_openapi

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if config.neural_network.mock:
    kobold_client = MockKoboldClient()
else:
    kobold_client = AsyncKoboldClient(
        url=config.neural_network.backend
    )

match config.neural_network.prompt_template:
    case PromptTemplateType.MISTRAL_V3:
        text_prompt_wrapper = MistralV7TextPrompt()

    case _:
        raise RuntimeError(f'Undefined text prompt template: {config.neural_network.prompt_template}')

generation_service = GenerationService(
    kobold_client=kobold_client,
    neural_network_config=config.neural_network,
    text_prompt_wrapper=text_prompt_wrapper
)
controller = Controller(generation_service)

app.include_router(controller.router)
