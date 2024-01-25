import logging
from logging import FileHandler
from logging import Logger

formatter = logging.Formatter("%(asctime)s %(message)s")


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> Logger:
    """
    Setting up a logger
    Arguments:
    - name: str
    - log_file: str
    - level = logging.info
    """
    handler: FileHandler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger: Logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
