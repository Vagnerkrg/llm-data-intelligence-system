from enum import Enum


class KnowledgeType(Enum):
    """
    Represents the type of knowledge acquired
    by the self-improvement system.
    """

    INSIGHT = "insight"

    PATTERN = "pattern"

    STRATEGY = "strategy"