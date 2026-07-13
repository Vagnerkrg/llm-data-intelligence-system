from enum import Enum


class DecisionStatus(str, Enum):
    """Represents the lifecycle of a cognitive decision."""

    PENDING = "pending"
    ANALYZING = "analyzing"
    SELECTED = "selected"
    COMMITTED = "committed"
    EVALUATED = "evaluated"
    COMPLETED = "completed"