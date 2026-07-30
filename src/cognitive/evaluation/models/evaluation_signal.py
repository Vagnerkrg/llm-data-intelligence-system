from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    """
    Tipos de sinais gerados pela avaliação.
    """

    IMPROVEMENT = "improvement"
    LEARNING = "learning"
    MEMORY = "memory"
    REFLECTION = "reflection"


@dataclass
class EvaluationSignal:
    """
    Sinal produzido após uma avaliação.
    """

    signal_type: SignalType

    message: str

    priority: float = 0.0