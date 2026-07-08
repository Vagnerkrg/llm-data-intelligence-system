from src.logging import Logger


class AppLogger:
    """
    High-level logging interface.

    Provides a centralized logging abstraction
    for the entire application.
    """


    def __init__(
        self,
        name: str
    ):

        self.logger = Logger.get_logger(
            name
        )


    def info(
        self,
        message: str
    ):

        self.logger.info(
            message
        )


    def warning(
        self,
        message: str
    ):

        self.logger.warning(
            message
        )


    def error(
        self,
        message: str
    ):

        self.logger.error(
            message
        )