from dataclasses import dataclass

from .policy_type import PolicyType


@dataclass
class Policy:
    """
    Represents a cognitive policy.
    """

    policy_type: PolicyType

    priority: int = 0

    description: str = ""

    enabled: bool = True

    def is_enabled(self) -> bool:
        return self.enabled