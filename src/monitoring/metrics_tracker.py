import json
import time
from datetime import datetime
from pathlib import Path


class MetricsTracker:
    """
    Tracks application execution metrics.

    Responsible for recording:
    - execution time
    - selected route
    - execution status
    - errors
    """


    def __init__(
        self,
        metrics_file="logs/application_metrics.jsonl"
    ):

        self.metrics_file = Path(
            metrics_file
        )

        self.metrics_file.parent.mkdir(
            exist_ok=True
        )

        self.start_time = None



    def start_timer(self):
        """
        Starts execution timer.
        """

        self.start_time = time.time()



    def stop_timer(self):
        """
        Returns execution duration.
        """

        if self.start_time is None:
            return 0


        return round(
            time.time() - self.start_time,
            4
        )



    def record(
        self,
        route: str,
        status: str = "success",
        error: str = None
    ):
        """
        Saves execution metrics.
        """


        metric = {

            "timestamp": datetime.now().isoformat(),

            "route": route,

            "execution_time":
                self.stop_timer(),

            "status": status,

            "error": error

        }


        with open(
            self.metrics_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    metric,
                    ensure_ascii=False
                )
                + "\n"
            )


        return metric