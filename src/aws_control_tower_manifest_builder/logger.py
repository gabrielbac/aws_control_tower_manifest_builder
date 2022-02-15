import logging
import sys
import os

APP_LOGGER_NAME = "aws-control-tower-manifest-builder"
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()


def setup_applevel_logger(logger_name=APP_LOGGER_NAME, file_name=None):
    logger = logging.getLogger(logger_name)
    level = logging.getLevelName(LOGLEVEL)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
