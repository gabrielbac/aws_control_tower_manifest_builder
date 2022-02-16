"""Setup Logging"""
import logging
import sys
import os

APP_LOGGER_NAME = "aws-control-tower-manifest-builder"
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()


def setup_applevel_logger(logger_name=APP_LOGGER_NAME, file_name=None):
    """
    Create and Setup logger

    Parameters:
    logger_name(string): Name of the logger
    file_name(string): Location to output logs too

    Return:
    logger from logging
    """
    logger = logging.getLogger(logger_name)
    level = logging.getLevelName(LOGLEVEL)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(stream_handler)
    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def get_logger(module_name):
    """Get logger for a given module name"""
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
