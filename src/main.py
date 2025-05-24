import logging
import logging.config
import yaml
from fastapi import FastAPI
from prometheus_client import make_asgi_app


def load_logging_config(config_file):
    """Load logging configuration from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    except FileNotFoundError:
        print(f"Logging config file '{config_file}' not found.")
    except yaml.YAMLError as e:
        print(f"Failed to parse YAML in logging config: {e}")
    except Exception as e:
        print(f"Error loading logging config: {e}")

# Load the logging configuration
load_logging_config('logging.yaml')

# Get the root logger
logger = logging.getLogger(__name__)

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

controller = Controller()

# Test logging
if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")  
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
