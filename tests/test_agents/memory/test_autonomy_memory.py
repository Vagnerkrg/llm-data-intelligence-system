from src.agents.memory.autonomy_memory import AutonomyMemory
from src.agents.autonomy.learning import LearningSignal



def test_autonomy_memory_stores_learning_signal():

    memory = AutonomyMemory()


    signal = LearningSignal(
        signal_id="learning-001",
        reflection_id="reflection-001",
        source="autonomy_engine",
        pattern="Successful execution pattern",
        impact="improved_strategy",
        confidence=0.9,
    )


    entry = memory.store_learning(
        signal
    )


    assert entry.key == "learning-001"

    assert (
        entry.memory_type
        ==
        "autonomy_learning"
    )



def test_autonomy_memory_retrieves_learning():

    memory = AutonomyMemory()


    signal = LearningSignal(
        signal_id="learning-002",
        reflection_id="reflection-002",
        source="autonomy_engine",
        pattern="Failure recovery",
        impact="adaptation",
        confidence=0.7,
    )


    memory.store_learning(
        signal
    )


    result = memory.get(
        "learning-002"
    )


    assert result is not None

    assert (
        result.value["pattern"]
        ==
        "Failure recovery"
    )



def test_autonomy_memory_count():

    memory = AutonomyMemory()


    assert memory.count() == 0