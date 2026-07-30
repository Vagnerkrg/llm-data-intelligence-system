from src.cognitive.evaluation.evaluator_registry import (
    EvaluatorRegistry
)


class DummyEvaluator:
    pass



def test_registry_creation():

    registry = EvaluatorRegistry()

    assert registry is not None



def test_register_evaluator():

    registry = EvaluatorRegistry()

    evaluator = DummyEvaluator()

    registry.register(
        "memory",
        evaluator
    )

    assert registry.exists(
        "memory"
    )



def test_get_evaluator():

    registry = EvaluatorRegistry()

    evaluator = DummyEvaluator()

    registry.register(
        "planner",
        evaluator
    )

    result = registry.get(
        "planner"
    )

    assert result == evaluator



def test_list_evaluators():

    registry = EvaluatorRegistry()

    registry.register(
        "execution",
        DummyEvaluator()
    )

    registry.register(
        "memory",
        DummyEvaluator()
    )


    items = registry.list_evaluators()

    assert len(items) == 2