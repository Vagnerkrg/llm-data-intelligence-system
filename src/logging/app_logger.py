from src.logging import Logger
from src.core.request_context import get_request_id



class AppLogger:
    """
    High-level logging interface.

    Provides a centralized logging abstraction
    with request tracing and structured metadata.
    """


    def __init__(
        self,
        name: str
    ):

        self.logger = Logger.get_logger(
            name
        )



    def _format_message(
        self,
        message: str,
        context: dict | None = None
    ) -> str:
        """
        Formats log messages with request context
        and optional structured metadata.
        """


        parts = []


        request_id = get_request_id()


        if request_id:

            parts.append(
                f"request_id={request_id}"
            )



        parts.append(
            message
        )



        if context:

            parts.append(
                str(context)
            )



        return " | ".join(
            parts
        )



    def info(
        self,
        message: str,
        context: dict | None = None
    ):

        self.logger.info(

            self._format_message(
                message,
                context
            )

        )



    def warning(
        self,
        message: str,
        context: dict | None = None
    ):

        self.logger.warning(

            self._format_message(
                message,
                context
            )

        )



    def error(
        self,
        message: str,
        context: dict | None = None
    ):

        self.logger.error(

            self._format_message(
                message,
                context
            )

        )