from dataclasses import dataclass

from .policy import Policy


@dataclass
class PolicyResult:
    """
    Result of applying a cognitive policy.
    """

    policy: Policy

    accepted: bool

    reason: str = ""

    def approved(self) -> bool:
        return self.accepted