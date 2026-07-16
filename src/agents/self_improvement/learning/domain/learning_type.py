"""Learning type definitions."""

from enum import Enum


class LearningType(Enum):
    """Types of cognitive learning."""

    PERFORMANCE = "performance"
    STRATEGY = "strategy"
    BEHAVIOR = "behavior"
    OPTIMIZATION = "optimization"
    PATTERN = "pattern"
    RULE = "rule"