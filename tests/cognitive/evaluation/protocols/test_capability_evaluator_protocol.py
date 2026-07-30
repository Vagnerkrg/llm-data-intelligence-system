from src.cognitive.evaluation.protocols.capability_evaluator import CapabilityEvaluator


class MockCapabilityEvaluator(CapabilityEvaluator):

    def evaluate(self, context):

        return {
            "score": 0.9
        }


def test_capability_evaluator_protocol_creation():

    evaluator = MockCapabilityEvaluator()

    assert evaluator is not None


def test_capability_evaluator_has_evaluate_method():

    evaluator = MockCapabilityEvaluator()

    assert hasattr(evaluator, "evaluate")


def test_capability_evaluator_execution():

    evaluator = MockCapabilityEvaluator()

    result = evaluator.evaluate(
        {
            "task": "reasoning"
        }
    )

    assert result["score"] == 0.9