import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_file = 'logs/app.log'):
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=5
    )
    console_handler = logging.StreamHandler()
    
    logging.basicConfig(
        level=logging.INFO,
        format=format,
        handlers=[
            file_handler,
            console_handler
        ]
    )
