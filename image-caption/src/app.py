from fastapi import FastAPI

from app_stuff import parse_arguments, setup_and_get_logger, get_neural_network_or_exit_on_error, get_result_cache
from controller.controller import Controller

app = FastAPI()

arguments = parse_arguments()

log = setup_and_get_logger('logging.yaml', arguments.log_level)

log.info('Loading model')

neural_network = get_neural_network_or_exit_on_error(arguments=arguments)

log.info('Done')

controller = Controller(
    network=neural_network,
    max_cached_results=arguments.max_responses_in_cache,
    cached_result_ttl=arguments.response_ttl,
    result_cache=get_result_cache(use_cache=arguments.use_result_cache, db_url=arguments.result_cache_db_url)
)

# Registering routes
app.include_router(controller.router)
