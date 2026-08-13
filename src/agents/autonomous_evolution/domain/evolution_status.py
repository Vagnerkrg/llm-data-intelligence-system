from enum import Enum


class EvolutionStatus(str, Enum):
    """
    Represents the lifecycle status of an autonomous evolution process.
    """

    PENDING = "pending"
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    COMPLETED = "completed"
    FAILED = "failed"