from src.cognitive.evaluation.evaluation_engine import (
    EvaluationEngine
)

from src.cognitive.evaluation.evaluator_registry import (
    EvaluatorRegistry
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult
)



class DummyEvaluator:


    def evaluate(
        self,
        context
    ):

        return EvaluationResult(
            score=1.0,
            passed=True,
            evaluator="dummy"
        )



def test_engine_creation():

    registry = EvaluatorRegistry()

    engine = EvaluationEngine(
        registry
    )

    assert engine is not None



def test_engine_single_evaluation():

    registry = EvaluatorRegistry()

    registry.register(
        "dummy",
        DummyEvaluator()
    )


    engine = EvaluationEngine(
        registry
    )


    context = EvaluationContext(
        agent_id="agent-001"
    )


    result = engine.evaluate(
        "dummy",
        context
    )


    assert result.passed is True
    assert result.score == 1.0



def test_engine_evaluate_all():

    registry = EvaluatorRegistry()


    registry.register(
        "dummy",
        DummyEvaluator()
    )


    engine = EvaluationEngine(
        registry
    )


    context = EvaluationContext(
        agent_id="agent-001"
    )


    results = engine.evaluate_all(
        context
    )


    assert len(results) == 1
    assert results[0].passed is True



def test_engine_missing_evaluator():

    registry = EvaluatorRegistry()

    engine = EvaluationEngine(
        registry
    )


    context = EvaluationContext(
        agent_id="agent-001"
    )


    try:

        engine.evaluate(
            "unknown",
            context
        )

        assert False

    except ValueError:

        assert True