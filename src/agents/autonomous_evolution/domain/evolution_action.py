from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EvolutionAction:
    """
    Represents a behavioral adaptation proposed by the evolution process.

    The domain describes the action but does not execute it.
    """

    action_type: str
    target: str
    parameters: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.action_type.strip():
            raise ValueError("Evolution action type cannot be empty.")

        if not self.target.strip():
            raise ValueError("Evolution action target cannot be empty.")

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evolution action into a dictionary.
        """
        return asdict(self)