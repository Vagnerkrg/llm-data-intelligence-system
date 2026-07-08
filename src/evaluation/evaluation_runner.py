import json

from pathlib import Path

from src.rag.query_engine import RAGQueryEngine



class EvaluationRunner:
    """
    Runs automated evaluation over RAG questions.

    Measures routing accuracy and retrieval behavior.
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


        for item in questions:

            response = self.rag.query(
                item["question"]
            )


            predicted = response["route"]["domain"]


            expected = item["expected_domain"]


            is_correct = (
                predicted == expected
            )


            if is_correct:

                correct += 1


            results.append(
                {
                    "question": item["question"],
                    "expected_domain": expected,
                    "predicted_domain": predicted,
                    "correct": is_correct,
                    "metrics": response["metrics"]
                }
            )


        report = {

            "total_questions": len(
                questions
            ),

            "correct_predictions": correct,

            "routing_accuracy": round(
                correct / len(questions),
                4
            ),

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