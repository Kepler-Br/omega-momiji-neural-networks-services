from fastapi import FastAPI

from app_stuff import get_neural_network_or_exit_on_error
from app_stuff import parse_arguments, setup_and_get_logger
from controller.controller import Controller

app = FastAPI()

arguments = parse_arguments()

log = setup_and_get_logger('logging.yaml', arguments.log_level)

neural_network = get_neural_network_or_exit_on_error(
    model_type=arguments.model_type,
    model_path=arguments.model_path,
    device_override=arguments.device_override
)

controller = Controller(
    network=neural_network,
    max_cached_responses=arguments.max_responses_in_cache,
    cached_responses_ttl=arguments.response_ttl,
)

# Registering routes
app.include_router(controller.router)
