"""
Application logging interface.

Provides a centralized logging abstraction
with support for standard and structured logs.
"""


from src.logging import Logger

from src.logging.structured_logger import StructuredLogger



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


        self.structured_logger = StructuredLogger(
            name
        )



    def info(
        self,
        message: str,
        context: dict | None = None
    ):

        if context:

            self.structured_logger.info(

                message,

                context

            )

            return


        self.logger.info(
            message
        )



    def warning(
        self,
        message: str,
        context: dict | None = None
    ):

        if context:

            self.structured_logger.warning(

                message,

                context

            )

            return


        self.logger.warning(
            message
        )



    def error(
        self,
        message: str,
        context: dict | None = None
    ):

        if context:

            self.structured_logger.error(

                message,

                context

            )

            return


        self.logger.error(
            message
        )