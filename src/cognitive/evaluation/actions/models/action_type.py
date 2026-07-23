from enum import Enum


class ActionType(str, Enum):
    """
    Types of actions that can be produced by the
    Cognitive Evaluation System.
    """

    ACCEPT = "accept"

    IMPROVE = "improve"

    RETRY = "retry"

    REPLAN = "replan"

    ESCALATE = "escalate"

    ABORT = "abort"