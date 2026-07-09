from typing import List

from src.agents.evaluation.routing_evaluator import RoutingEvaluation



class RoutingHistory:
    """
    Stores routing evaluation records.

    Provides a simple in-memory history layer
    for monitoring router behavior.
    """


    def __init__(self):

        self._records: List[RoutingEvaluation] = []



    def add(
        self,
        evaluation: RoutingEvaluation
    ):
        """
        Store a routing evaluation record.
        """

        self._records.append(
            evaluation
        )



    def all(
        self
    ) -> List[RoutingEvaluation]:
        """
        Return all stored evaluations.
        """

        return self._records



    def count(
        self
    ) -> int:
        """
        Return number of stored evaluations.
        """

        return len(
            self._records
        )