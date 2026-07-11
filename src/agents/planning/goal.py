from typing import Dict, List, Optional


class Goal:
    """
    Represents the objective that drives
    agent execution planning.

    The goal is generated from reasoning
    output and consumed by planning layers.
    """

    def __init__(
        self,
        objective: str,
        intent: str = "general",
        required_capabilities: Optional[List[str]] = None,
        strategy: str = "default",
        constraints: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Create execution goal.
        """


        self.objective = objective


        self.intent = intent


        self.required_capabilities = (
            required_capabilities
            if required_capabilities
            else []
        )


        self.strategy = strategy


        self.constraints = (
            constraints
            if constraints
            else {}
        )


        self.metadata = (
            metadata
            if metadata
            else {}
        )


    def add_capability(
        self,
        capability: str
    ):
        """
        Add required capability.
        """

        if capability not in self.required_capabilities:

            self.required_capabilities.append(
                capability
            )


    def add_constraint(
        self,
        key: str,
        value
    ):
        """
        Add execution constraint.
        """

        self.constraints[key] = value


    def to_dict(
        self
    ):
        """
        Serialize goal information.
        """

        return {

            "objective": self.objective,

            "intent": self.intent,

            "required_capabilities":
                self.required_capabilities,

            "strategy":
                self.strategy,

            "constraints":
                self.constraints,

            "metadata":
                self.metadata

        }


    def __repr__(
        self
    ):
        return (
            "Goal("
            f"objective={self.objective!r}, "
            f"intent={self.intent!r}"
            ")"
        )