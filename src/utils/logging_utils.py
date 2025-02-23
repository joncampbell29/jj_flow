import logging
import logging.config
import yaml

def setup_logging(logger_name='data_pipeline'):
    try:
        with open('config/logging_config.yaml', 'r') as fil:
            config = yaml.safe_load(fil)
        logging.config.dictConfig(config)
        return logging.getLogger(logger_name)
    except Exception as e:
        print(f"Failed to load logging configuration: {e}")
        return logging.getLogger(__name__)