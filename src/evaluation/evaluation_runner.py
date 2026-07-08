import json
import sys

from pathlib import Path

from src.rag.query_engine import RAGQueryEngine



class EvaluationRunner:
    """
    Runs automated evaluation over RAG benchmarks.

    Supports multiple evaluation datasets
    and measures routing accuracy,
    retrieval quality and fallback behavior.
    """



    def __init__(
        self,
        questions_path=None,
        output_path="evaluation_report.json"
    ):

        self.questions_path = Path(
            questions_path
            if questions_path
            else "tests/evaluation/rag_questions.json"
        )


        self.output_path = Path(
            output_path
        )


        self.rag = RAGQueryEngine()



    def load_questions(self):
        """
        Loads evaluation benchmark questions.
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
        Executes benchmark evaluation.
        """

        questions = self.load_questions()


        results = []


        correct = 0

        retrieval_scores = []

        fallback_count = 0


        domain_stats = {}



        for item in questions:


            response = self.rag.query(
                item["question"]
            )


            predicted = (
                response["route"]["domain"]
            )


            expected = (
                item["expected_domain"]
            )


            is_correct = (
                predicted == expected
            )


            if is_correct:

                correct += 1



            metrics = response["metrics"]


            retrieval_scores.append(
                metrics["best_score"]
            )


            if metrics["fallback_used"]:

                fallback_count += 1



            if expected not in domain_stats:

                domain_stats[expected] = {

                    "questions": 0,

                    "correct": 0,

                    "scores": []

                }



            domain_stats[expected]["questions"] += 1


            if is_correct:

                domain_stats[expected]["correct"] += 1



            domain_stats[expected]["scores"].append(
                metrics["best_score"]
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



        formatted_domain_metrics = {}



        for domain, stats in domain_stats.items():


            formatted_domain_metrics[domain] = {

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
                sum(retrieval_scores) / len(retrieval_scores),
                4
            ),


            "fallback_rate": round(
                fallback_count / len(questions),
                4
            ),


            "domain_metrics": formatted_domain_metrics,


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


    questions_path = None



    if len(sys.argv) > 1:

        questions_path = sys.argv[1]



    runner = EvaluationRunner(
        questions_path=questions_path
    )



    result = runner.run()



    print(

        json.dumps(

            result,

            ensure_ascii=False,

            indent=4

        )

    )