from src.cognitive.evaluation.evaluation_pipeline import (
    EvaluationPipeline
)

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
            score=0.9,
            passed=True,
            evaluator="dummy"
        )



def create_pipeline():

    registry = EvaluatorRegistry()

    registry.register(
        "dummy",
        DummyEvaluator()
    )


    engine = EvaluationEngine(
        registry
    )


    return EvaluationPipeline(
        engine
    )



def test_pipeline_creation():

    pipeline = create_pipeline()

    assert pipeline is not None



def test_pipeline_run():

    pipeline = create_pipeline()


    context = EvaluationContext(
        agent_id="agent-001"
    )


    results = pipeline.run(
        context
    )


    assert len(results) == 1
    assert results[0].passed is True



def test_pipeline_run_single():

    pipeline = create_pipeline()


    context = EvaluationContext(
        agent_id="agent-001"
    )


    result = pipeline.run_single(
        "dummy",
        context
    )


    assert result.score == 0.9



def test_pipeline_invalid_evaluator():

    pipeline = create_pipeline()


    context = EvaluationContext(
        agent_id="agent-001"
    )


    try:

        pipeline.run_single(
            "unknown",
            context
        )

        assert False

    except ValueError:

        assert True