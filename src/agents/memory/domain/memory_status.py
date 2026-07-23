from enum import Enum


class MemoryStatus(Enum):
    """
    Represents the lifecycle status
    of a memory operation.
    """

    CREATED = "created"

    STORED = "stored"

    RETRIEVED = "retrieved"

    FAILED = "failed"