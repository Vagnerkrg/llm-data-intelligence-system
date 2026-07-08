import json
from datetime import datetime
from pathlib import Path


class EvaluationHistory:
    """
    Stores evaluation results history.

    Persists evaluation events in JSONL format
    for future analysis and monitoring.
    """


    def __init__(
        self,
        file_path="logs/evaluation_history.jsonl"
    ):

        self.file_path = Path(
            file_path
        )

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )



    def save(
        self,
        data: dict
    ):
        """
        Saves evaluation event.
        """


        record = {

            "timestamp": datetime.now().isoformat(),

            **data

        }


        with open(
            self.file_path,
            "a",
            encoding="utf-8"
        ) as file:


            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
            )

            file.write(
                "\n"
            )


        return record



    def read_all(self):
        """
        Returns stored evaluation history.
        """


        if not self.file_path.exists():

            return []



        records = []


        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:


            for line in file:

                records.append(
                    json.loads(line)
                )


        return records