from src.agents.memory.intelligence.memory_policy import (
    MemoryPolicy
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)


def test_should_return_high_priority_for_long_term_memory():

    policy = MemoryPolicy()


    priority = policy.get_priority(
        MemoryType.LONG_TERM
    )


    assert priority == 1.0



def test_should_return_medium_priority_for_short_term_memory():

    policy = MemoryPolicy()


    priority = policy.get_priority(
        MemoryType.SHORT_TERM
    )


    assert priority == 0.5



def test_should_retain_memory_above_threshold():

    policy = MemoryPolicy()


    result = policy.should_retain(
        0.8
    )


    assert result is True



def test_should_not_retain_low_priority_memory():

    policy = MemoryPolicy()


    result = policy.should_retain(
        0.2
    )


    assert result is False