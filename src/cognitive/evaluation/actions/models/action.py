from dataclasses import dataclass, field

from .action_type import ActionType


@dataclass
class Action:
    """
    Represents an action selected after
    cognitive evaluation.
    """

    action_type: ActionType

    priority: int = 0

    reason: str = ""

    metadata: dict = field(default_factory=dict)

    def is_terminal(self) -> bool:
        """
        Returns True if this action finishes
        the current execution flow.
        """

        return self.action_type in {
            ActionType.ACCEPT,
            ActionType.ABORT,
        }

    def requires_retry(self) -> bool:
        """
        Indicates whether execution
        should be attempted again.
        """

        return self.action_type in {
            ActionType.RETRY,
            ActionType.REPLAN,
        }