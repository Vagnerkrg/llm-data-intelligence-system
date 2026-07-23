from src.agents.memory.domain.memory_type import (
    MemoryType
)


def test_should_have_expected_memory_types():

    assert MemoryType.SHORT_TERM.value == (
        "short_term"
    )

    assert MemoryType.LONG_TERM.value == (
        "long_term"
    )

    assert MemoryType.EPISODIC.value == (
        "episodic"
    )

    assert MemoryType.SEMANTIC.value == (
        "semantic"
    )

    assert MemoryType.PROCEDURAL.value == (
        "procedural"
    )