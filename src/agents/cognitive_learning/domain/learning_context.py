from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LearningContext:
    """Context consumed by the cognitive learning layer."""

    context_id: str
    experiences: tuple[Any, ...] = ()
    signals: tuple[Any, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.context_id.strip():
            raise ValueError("context_id must not be empty.")

        if isinstance(self.experiences, list):
            object.__setattr__(
                self,
                "experiences",
                tuple(self.experiences),
            )

        if isinstance(self.signals, list):
            object.__setattr__(
                self,
                "signals",
                tuple(self.signals),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "experiences": list(self.experiences),
            "signals": list(self.signals),
            "metadata": dict(self.metadata),
        }
