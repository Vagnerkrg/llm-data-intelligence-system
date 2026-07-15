from enum import Enum


class EvaluationCriterion(str, Enum):
    """
    Criteria used to evaluate agent execution quality.
    """

    ACCURACY = "accuracy"

    EFFICIENCY = "efficiency"

    CONSISTENCY = "consistency"

    RELIABILITY = "reliability"

    EXPLAINABILITY = "explainability"