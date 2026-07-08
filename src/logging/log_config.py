import logging
from pathlib import Path


LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)


LOG_FILE = LOG_DIRECTORY / "application.log"


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)