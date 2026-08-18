from enum import Enum


class LearningStatus(str, Enum):
    """Lifecycle states of a cognitive learning operation."""

    PENDING = "pending"
    PROCESSING = "processing"
    LEARNED = "learned"
    REJECTED = "rejected"

