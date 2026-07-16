from typing import Dict

from .models import ExecutionRecord


class ExecutionStore:
    """
    Temporary in-memory execution storage.

    Future versions may replace this with:
    - database storage
    - vector memory
    - analytics warehouse
    """

    def __init__(self):
        self._executions: Dict[str, ExecutionRecord] = {}

    def save(
        self,
        execution: ExecutionRecord
    ) -> None:
        self._executions[
            execution.execution_id
        ] = execution

    def get(
        self,
        execution_id: str
    ) -> ExecutionRecord | None:

        return self._executions.get(
            execution_id
        )

    def list_all(
        self
    ) -> list[ExecutionRecord]:

        return list(
            self._executions.values()
        )