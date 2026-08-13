from dataclasses import asdict, dataclass, field
from typing import Any

from .evolution_action import EvolutionAction
from .evolution_status import EvolutionStatus


@dataclass(slots=True)
class EvolutionResult:
    """
    Represents the result of an autonomous evolution process.

    The result describes what happened; it does not execute or determine
    the evolution itself.
    """

    status: EvolutionStatus = EvolutionStatus.PENDING
    success: bool = False
    action: EvolutionAction | None = None
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.status, EvolutionStatus):
            raise TypeError(
                "status must be an EvolutionStatus instance."
            )

        if self.action is not None and not isinstance(
            self.action,
            EvolutionAction,
        ):
            raise TypeError(
                "action must be an EvolutionAction instance or None."
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evolution result into a dictionary.
        """
        data = asdict(self)
        data["status"] = self.status.value

        return data