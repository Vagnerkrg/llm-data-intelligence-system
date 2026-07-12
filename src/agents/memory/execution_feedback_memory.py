from typing import List

from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)


class ExecutionFeedbackMemory:
    """
    Stores execution feedback history.

    This memory allows future components
    to analyze previous execution outcomes.
    """

    def __init__(self):
        self._feedbacks: List[ExecutionFeedback] = []


    def add(
        self,
        feedback: ExecutionFeedback,
    ):
        """
        Store a new execution feedback.
        """

        self._feedbacks.append(
            feedback
        )


    def all(
        self
    ) -> List[ExecutionFeedback]:
        """
        Return all stored feedback entries.
        """

        return self._feedbacks.copy()


    def last(
        self
    ) -> ExecutionFeedback | None:
        """
        Return latest feedback.
        """

        if not self._feedbacks:
            return None


        return self._feedbacks[-1]


    def count(
        self
    ) -> int:
        """
        Return number of stored feedback entries.
        """

        return len(
            self._feedbacks
        )


    def clear(
        self
    ):
        """
        Clear feedback history.
        """

        self._feedbacks.clear()