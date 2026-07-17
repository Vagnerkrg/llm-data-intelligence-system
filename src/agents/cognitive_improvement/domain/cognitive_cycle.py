from enum import Enum


class CognitiveCycle(str, Enum):
    EVALUATION = "evaluation"
    REFLECTION = "reflection"
    LEARNING = "learning"
    KNOWLEDGE = "knowledge"
    ADAPTATION = "adaptation"
    COMPLETED = "completed"
    FAILED = "failed"