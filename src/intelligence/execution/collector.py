import uuid
from datetime import datetime, timezone

from .events import ExecutionEvent

from .models import (
    ExecutionRecord,
    ExecutionStep,
    ExecutionMetric,
)

from .store import ExecutionStore


class ExecutionCollector:
    """
    Captures execution lifecycle information.

    Observes execution without controlling it.
    """

    def __init__(
        self,
        store: ExecutionStore
    ):

        self.store = store


    def start_execution(
        self,
        request: str
    ) -> str:

        execution_id = str(uuid.uuid4())

        record = ExecutionRecord(
            execution_id=execution_id,
            request=request,
            started_at=datetime.now(
                timezone.utc
            ),
        )

        self.store.save(record)

        return execution_id


    def record_event(
        self,
        event: ExecutionEvent
    ):

        execution = self.store.get(
            event.execution_id
        )

        if execution is None:
            return


        step = ExecutionStep(
            component=event.component,
            action=event.event_type.value,
            output_data=event.payload,
            status="completed",
        )

        execution.steps.append(step)

        self.store.save(
            execution
        )


    def add_metric(
        self,
        execution_id: str,
        metric_name: str,
        metric_value,
        category: str = "general",
    ):

        execution = self.store.get(
            execution_id
        )

        if execution is None:
            return


        execution.metrics.append(
            ExecutionMetric(
                metric_name=metric_name,
                metric_value=metric_value,
                category=category,
            )
        )

        self.store.save(
            execution
        )


    def finish_execution(
        self,
        execution_id: str,
        status: str = "completed"
    ):

        execution = self.store.get(
            execution_id
        )

        if execution is None:
            return


        execution.status = status

        execution.finished_at = datetime.now(
            timezone.utc
        )

        self.store.save(
            execution
        )