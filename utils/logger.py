import logging

from config import LOG_DIR


def configure_logger():
    logger = logging.getLogger("automation")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    file_handler = logging.FileHandler(
        f"{LOG_DIR}/automation.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger