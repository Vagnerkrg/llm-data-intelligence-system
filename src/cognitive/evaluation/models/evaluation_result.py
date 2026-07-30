from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class EvaluationResult:
    """
    Resultado final de uma avaliação cognitiva.
    """

    score: float

    passed: bool

    evaluator: str

    details: Dict[str, Any] = field(default_factory=dict)

    confidence: float = 0.0

    def add_detail(self, key: str, value: Any) -> None:
        self.details[key] = value

    def is_successful(self) -> bool:
        return self.passed and self.score > 0