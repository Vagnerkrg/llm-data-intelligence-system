import json

from pathlib import Path


class DashboardMetrics:
    """
    Aggregates application execution metrics.

    Reads the application metrics log and
    generates summary statistics.
    """

    def __init__(
        self,
        metrics_file="logs/application_metrics.jsonl"
    ):

        self.metrics_file = Path(
            metrics_file
        )


    def load(self):

        if not self.metrics_file.exists():

            return []


        records = []


        with open(
            self.metrics_file,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if line:

                    records.append(
                        json.loads(line)
                    )


        return records


    def summary(self):

        records = self.load()


        if not records:

            return {

                "total_requests": 0,

                "success_rate": 0,

                "error_rate": 0,

                "average_execution_time": 0,

                "routes": {}

            }


        total = len(records)


        success = sum(

            1

            for item in records

            if item["status"] == "success"

        )


        errors = total - success


        average_time = round(

            sum(

                item["execution_time"]

                for item in records

            )

            / total,

            4

        )


        routes = {}


        for item in records:

            route = item["route"]

            routes[route] = (

                routes.get(route, 0)

                + 1

            )


        return {

            "total_requests": total,

            "success_rate": round(

                success / total,

                4

            ),

            "error_rate": round(

                errors / total,

                4

            ),

            "average_execution_time": average_time,

            "routes": routes

        }