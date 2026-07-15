from enum import Enum


class AdaptationType(Enum):
    """
    Defines the type of adaptation applied by the self-improvement system.
    """

    STRATEGY = "strategy"

    POLICY = "policy"

    BEHAVIOR = "behavior"

    TOOL_SELECTION = "tool_selection"

    EXECUTION_FLOW = "execution_flow"