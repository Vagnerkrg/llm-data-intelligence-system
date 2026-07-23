from enum import Enum


class PolicyType(str, Enum):
    """
    Supported cognitive policy types.
    """

    AUTOMATIC = "automatic"

    HUMAN_REVIEW = "human_review"

    SAFE_MODE = "safe_mode"

    REPLAN = "replan"

    ABORT = "abort"