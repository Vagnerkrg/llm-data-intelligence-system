"""
Structured logging utilities.

Provides contextual logging support
for production observability.
"""


import json

import logging

from datetime import datetime, timezone



class StructuredLogger:
    """
    Structured logger wrapper.

    Generates JSON formatted logs
    with execution context.
    """


    def __init__(
        self,
        name: str
    ):

        self.logger = logging.getLogger(
            name
        )



    def _format(
        self,
        level: str,
        event: str,
        context: dict | None = None
    ):

        payload = {

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "level":
                level,

            "event":
                event

        }


        if context:

            payload.update(
                context
            )


        return json.dumps(
            payload,
            ensure_ascii=False
        )



    def info(
        self,
        event: str,
        context: dict | None = None
    ):

        self.logger.info(

            self._format(

                level="INFO",

                event=event,

                context=context

            )

        )



    def error(
        self,
        event: str,
        context: dict | None = None
    ):

        self.logger.error(

            self._format(

                level="ERROR",

                event=event,

                context=context

            )

        )



    def warning(
        self,
        event: str,
        context: dict | None = None
    ):

        self.logger.warning(

            self._format(

                level="WARNING",

                event=event,

                context=context

            )

        )