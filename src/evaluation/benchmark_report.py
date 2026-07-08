from typing import Dict, List

import json

from pathlib import Path



class BenchmarkReport:
    """
    Generates consolidated reports
    from answer evaluation results.
    """


    def __init__(
        self,
        output_path="answer_quality_report.json"
    ):

        self.output_path = Path(
            output_path
        )



    def generate(
        self,
        evaluations: List[Dict]
    ) -> Dict:
        """
        Creates benchmark summary.
        """


        if not evaluations:

            return {}



        total = len(
            evaluations
        )


        average_quality = sum(

            item["quality_score"]

            for item in evaluations

        ) / total



        average_faithfulness = sum(

            item["faithfulness"]

            for item in evaluations

        ) / total



        average_completeness = sum(

            item["completeness"]

            for item in evaluations

        ) / total



        average_relevance = sum(

            item["context_relevance"]

            for item in evaluations

        ) / total



        report = {

            "total_answers": total,

            "average_quality_score": round(
                average_quality,
                4
            ),

            "average_faithfulness": round(
                average_faithfulness,
                4
            ),

            "average_completeness": round(
                average_completeness,
                4
            ),

            "average_context_relevance": round(
                average_relevance,
                4
            ),

            "results": evaluations

        }



        self.save(
            report
        )


        return report



    def save(
        self,
        report: Dict
    ):
        """
        Saves benchmark report.
        """


        with open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                ensure_ascii=False,
                indent=4
            )