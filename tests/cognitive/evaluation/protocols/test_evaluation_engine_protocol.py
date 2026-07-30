from src.cognitive.evaluation.protocols.evaluation_engine import EvaluationEngine


class MockEvaluationEngine(EvaluationEngine):

    def evaluate(self, context):

        return {
            "status": "completed"
        }


def test_evaluation_engine_protocol_creation():

    engine = MockEvaluationEngine()

    assert engine is not None


def test_evaluation_engine_has_evaluate_method():

    engine = MockEvaluationEngine()

    assert hasattr(engine, "evaluate")


def test_evaluation_engine_execution():

    engine = MockEvaluationEngine()

    result = engine.evaluate(
        {
            "execution_id": "exec-001"
        }
    )

    assert result["status"] == "completed"