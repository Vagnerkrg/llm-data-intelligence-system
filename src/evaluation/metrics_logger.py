import json

from pathlib import Path
from datetime import datetime



class MetricsLogger:
    """
    Persists RAG execution metrics.

    Stores one JSON object per line,
    enabling future analysis and evaluation.
    """



    def __init__(
        self,
        log_path="logs/rag_metrics.jsonl"
    ):

        self.log_path = Path(
            log_path
        )



    def log(
        self,
        metrics: dict
    ):
        """
        Saves metrics to JSONL file.
        """


        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        record = {

            "timestamp": datetime.now().isoformat(),

            **metrics

        }


        with open(
            self.log_path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(

                json.dumps(
                    record,
                    ensure_ascii=False
                )

                + "\n"

            )


        return record