import logging
import os
from logging import FileHandler
from logging import Logger


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> Logger:
    """
    Setting up a logger
    Arguments:
    - name: str
    - log_file: str
    - level = logging.info
    """
    default_log_dir = "logs/"

    if not os.path.isdir(default_log_dir):
        os.makedirs(default_log_dir)

    log_file_path = os.path.join(default_log_dir, log_file)

    logger: Logger = logging.getLogger(name)
    logger.setLevel(level)

    handler: FileHandler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
