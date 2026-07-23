from src.cognitive.evaluation.signals.memory_signal import MemorySignal


def test_memory_signal_creation():

    signal = MemorySignal(
        action="store",
        content="Important execution pattern"
    )

    assert signal.action == "store"
    assert signal.content == "Important execution pattern"


def test_memory_signal_importance():

    signal = MemorySignal(
        action="update",
        content="Memory update",
        importance=0.8
    )

    assert signal.importance == 0.8