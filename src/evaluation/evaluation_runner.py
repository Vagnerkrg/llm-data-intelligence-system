import json

from pathlib import Path

from collections import defaultdict

from src.rag.query_engine import RAGQueryEngine



class EvaluationRunner:
    """
    Runs automated evaluation over RAG questions.

    Measures:
    - routing accuracy
    - retrieval quality
    - fallback usage
    - domain performance
    """



    def __init__(
        self,
        questions_path="tests/evaluation/rag_questions.json",
        output_path="evaluation_report.json"
    ):

        self.questions_path = Path(
            questions_path
        )

        self.output_path = Path(
            output_path
        )

        self.rag = RAGQueryEngine()



    def load_questions(self):
        """
        Loads evaluation dataset.
        """

        with open(
            self.questions_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )



    def run(self):
        """
        Executes evaluation.
        """

        questions = self.load_questions()


        results = []


        correct = 0

        total_scores = []

        fallback_count = 0


        domain_stats = defaultdict(
            lambda: {
                "questions": 0,
                "correct": 0,
                "scores": []
            }
        )



        for item in questions:


            response = self.rag.query(
                item["question"]
            )


            predicted = response["route"]["domain"]

            expected = item["expected_domain"]


            metrics = response["metrics"]


            is_correct = (
                predicted == expected
            )


            if is_correct:

                correct += 1



            if metrics["fallback_used"]:

                fallback_count += 1



            score = metrics["best_score"]

            total_scores.append(
                score
            )



            domain_stats[expected]["questions"] += 1


            if is_correct:

                domain_stats[expected]["correct"] += 1


            domain_stats[expected]["scores"].append(
                score
            )



            results.append(

                {
                    "question": item["question"],

                    "expected_domain": expected,

                    "predicted_domain": predicted,

                    "correct": is_correct,

                    "metrics": metrics

                }

            )



        domain_metrics = {}



        for domain, stats in domain_stats.items():


            domain_metrics[domain] = {

                "questions": stats["questions"],

                "accuracy": round(
                    stats["correct"] / stats["questions"],
                    4
                ),

                "average_score": round(
                    sum(stats["scores"]) / len(stats["scores"]),
                    4
                )

            }



        report = {


            "total_questions": len(
                questions
            ),


            "correct_predictions": correct,


            "routing_accuracy": round(
                correct / len(questions),
                4
            ),


            "average_retrieval_score": round(
                sum(total_scores) / len(total_scores),
                4
            ),


            "fallback_rate": round(
                fallback_count / len(questions),
                4
            ),


            "domain_metrics": domain_metrics,


            "results": results

        }



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



        return report





if __name__ == "__main__":


    runner = EvaluationRunner()


    result = runner.run()


    print(

        json.dumps(
            result,
            ensure_ascii=False,
            indent=4
        )

    )