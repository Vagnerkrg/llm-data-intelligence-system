from dataclasses import dataclass, field

from .action import Action


@dataclass
class ActionResult:
    """
    Result returned by the Action Engine.
    """

    action: Action

    executed: bool = False

    message: str = ""

    metadata: dict = field(default_factory=dict)

    def mark_executed(self):
        self.executed = True

    def succeeded(self) -> bool:
        return self.executed