from src.agents.cognitive_improvement.services.cycle_executor import (
    CycleExecutor,
)


def test_should_create_cycle_executor():
    executor = CycleExecutor()

    assert executor is not None