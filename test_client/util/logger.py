import logging
import os


def get_logger(name: str) -> logging.Logger:
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers:  # Avoid adding duplicate handlers
        logger.addHandler(console_handler)

    return logger
