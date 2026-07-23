from enum import Enum


class MemoryType(Enum):
    """
    Represents different types
    of agent memory.
    """

    SHORT_TERM = "short_term"

    LONG_TERM = "long_term"

    EPISODIC = "episodic"

    SEMANTIC = "semantic"

    PROCEDURAL = "procedural"