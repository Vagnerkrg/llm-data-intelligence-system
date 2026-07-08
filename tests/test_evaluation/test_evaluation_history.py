from src.evaluation.evaluation_history import EvaluationHistory



class TestEvaluationHistory:


    def test_save_and_read_history(
        self,
        tmp_path
    ):

        file_path = (
            tmp_path /
            "evaluation_history.jsonl"
        )


        history = EvaluationHistory(
            file_path
        )


        result = history.save(
            {
                "route": "rag",
                "score": 0.9
            }
        )


        assert result["route"] == "rag"


        records = history.read_all()


        assert len(records) == 1

        assert records[0]["score"] == 0.9