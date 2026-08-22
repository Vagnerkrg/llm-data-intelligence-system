"""SQLite repository implementations for Observability."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import List, Optional

from src.observability.contracts.storage import (
    ErrorRepository,
    EventRepository,
    MetricsRepository,
    ObservabilityRepository,
    TraceRepository,
)
from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionState,
    ExecutionTrace,
)
from src.observability.infrastructure.storage.sqlite_store import (
    SQLiteObservabilityStore,
)


def _json(value) -> str:
    """Serialize a value to JSON."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def _load_json(value: str):
    """Deserialize JSON."""
    return json.loads(value)


def _optional_json(value):
    """Deserialize optional JSON."""
    if value is None:
        return None

    return _load_json(value)


class SQLiteTraceRepository(TraceRepository):
    """Persist execution traces in SQLite."""

    def __init__(
        self,
        store: SQLiteObservabilityStore,
    ) -> None:
        self.store = store

    def save(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionTrace:
        """Persist a complete trace snapshot."""
        payload = trace.to_dict()

        with self.store.connection() as connection:
            connection.execute(
                """
                INSERT INTO execution_traces (
                    execution_id,
                    status,
                    started_at,
                    finished_at,
                    context_json,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(execution_id)
                DO UPDATE SET
                    status = excluded.status,
                    started_at = excluded.started_at,
                    finished_at = excluded.finished_at,
                    context_json = excluded.context_json,
                    metadata_json = excluded.metadata_json
                """,
                (
                    trace.execution_id,
                    trace.status.value,
                    self._timestamp(trace.started_at),
                    self._timestamp(trace.finished_at),
                    _json(trace.context.to_dict())
                    if trace.context is not None
                    else None,
                    _json(payload["metadata"]),
                ),
            )

        return deepcopy(trace)

    def get(
        self,
        execution_id: str,
    ) -> Optional[ExecutionTrace]:
        """Retrieve a trace without child records."""
        with self.store.connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM execution_traces
                WHERE execution_id = ?
                """,
                (execution_id,),
            ).fetchone()

        if row is None:
            return None

        return ExecutionTrace(
            execution_id=row["execution_id"],
            status=row["status"],
            started_at=row["started_at"],
            finished_at=row["finished_at"],
            context=(
                self._context(
                    row["context_json"],
                )
                if row["context_json"]
                else None
            ),
            metadata=_load_json(row["metadata_json"]),
        )

    def list(
        self,
        *,
        limit: Optional[int] = None,
    ) -> List[ExecutionTrace]:
        """List traces by newest start time."""
        query = """
            SELECT *
            FROM execution_traces
            ORDER BY
                CASE
                    WHEN started_at IS NULL THEN 1
                    ELSE 0
                END,
                started_at DESC,
                execution_id DESC
        """

        params = ()

        if limit is not None:
            if limit <= 0:
                raise ValueError("limit must be greater than zero.")

            query += " LIMIT ?"
            params = (limit,)

        with self.store.connection() as connection:
            rows = connection.execute(
                query,
                params,
            ).fetchall()

        return [self._row_to_trace(row) for row in rows]

    def delete(
        self,
        execution_id: str,
    ) -> bool:
        """Delete a trace."""
        with self.store.connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM execution_traces
                WHERE execution_id = ?
                """,
                (execution_id,),
            )

            return cursor.rowcount > 0

    @staticmethod
    def _timestamp(value) -> Optional[str]:
        if value is None:
            return None

        return value.isoformat()

    @staticmethod
    def _context(value):
        from src.observability.domain.models import (
            ObservabilityContext,
        )

        return ObservabilityContext.from_json(value)

    @classmethod
    def _row_to_trace(
        cls,
        row,
    ) -> ExecutionTrace:
        return ExecutionTrace(
            execution_id=row["execution_id"],
            status=row["status"],
            started_at=row["started_at"],
            finished_at=row["finished_at"],
            context=(
                cls._context(
                    row["context_json"],
                )
                if row["context_json"]
                else None
            ),
            metadata=_load_json(row["metadata_json"]),
        )


class SQLiteEventRepository(EventRepository):
    """Persist execution events in SQLite."""

    def __init__(
        self,
        store: SQLiteObservabilityStore,
    ) -> None:
        self.store = store

    def save(
        self,
        event: ExecutionEvent,
    ) -> ExecutionEvent:
        with self.store.connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO execution_events (
                    event_id,
                    execution_id,
                    event_type,
                    timestamp,
                    component,
                    stage,
                    status,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.execution_id,
                    event.event_type.value,
                    event.timestamp.isoformat(),
                    event.component,
                    event.stage,
                    (event.status.value if event.status is not None else None),
                    _json(event.metadata),
                ),
            )

        return deepcopy(event)

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionEvent]:
        with self.store.connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM execution_events
                WHERE execution_id = ?
                ORDER BY timestamp ASC, event_id ASC
                """,
                (execution_id,),
            ).fetchall()

        return [
            ExecutionEvent.from_dict(
                {
                    "event_id": row["event_id"],
                    "execution_id": row["execution_id"],
                    "event_type": row["event_type"],
                    "timestamp": row["timestamp"],
                    "component": row["component"],
                    "stage": row["stage"],
                    "status": row["status"],
                    "metadata": _load_json(row["metadata_json"]),
                }
            )
            for row in rows
        ]

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        with self.store.connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM execution_events
                WHERE execution_id = ?
                """,
                (execution_id,),
            )

            return cursor.rowcount


class SQLiteMetricsRepository(MetricsRepository):
    """Persist execution metrics in SQLite."""

    def __init__(
        self,
        store: SQLiteObservabilityStore,
    ) -> None:
        self.store = store

    def save(
        self,
        metric: ExecutionMetric,
    ) -> ExecutionMetric:
        with self.store.connection() as connection:
            connection.execute(
                """
                INSERT INTO execution_metrics (
                    execution_id,
                    metric_name,
                    value,
                    unit,
                    timestamp,
                    component,
                    metric_type,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    metric.execution_id,
                    metric.metric_name,
                    metric.value,
                    metric.unit,
                    metric.timestamp.isoformat(),
                    metric.component,
                    metric.metric_type.value,
                    _json(metric.metadata),
                ),
            )

        return deepcopy(metric)

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionMetric]:
        with self.store.connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM execution_metrics
                WHERE execution_id = ?
                ORDER BY timestamp ASC, id ASC
                """,
                (execution_id,),
            ).fetchall()

        return [
            ExecutionMetric.from_dict(
                {
                    "metric_name": row["metric_name"],
                    "value": row["value"],
                    "unit": row["unit"],
                    "timestamp": row["timestamp"],
                    "execution_id": row["execution_id"],
                    "component": row["component"],
                    "metric_type": row["metric_type"],
                    "metadata": _load_json(row["metadata_json"]),
                }
            )
            for row in rows
        ]

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        with self.store.connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM execution_metrics
                WHERE execution_id = ?
                """,
                (execution_id,),
            )

            return cursor.rowcount


class SQLiteErrorRepository(ErrorRepository):
    """Persist execution errors in SQLite."""

    def __init__(
        self,
        store: SQLiteObservabilityStore,
    ) -> None:
        self.store = store

    def save(
        self,
        error: ExecutionError,
    ) -> ExecutionError:
        with self.store.connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO execution_errors (
                    error_id,
                    execution_id,
                    timestamp,
                    component,
                    stage,
                    severity,
                    error_type,
                    message,
                    recoverable,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    error.error_id,
                    error.execution_id,
                    error.timestamp.isoformat(),
                    error.component,
                    error.stage,
                    error.severity.value,
                    error.error_type,
                    error.message,
                    int(error.recoverable),
                    _json(error.metadata),
                ),
            )

        return deepcopy(error)

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionError]:
        with self.store.connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM execution_errors
                WHERE execution_id = ?
                ORDER BY timestamp ASC, error_id ASC
                """,
                (execution_id,),
            ).fetchall()

        return [
            ExecutionError.from_dict(
                {
                    "error_id": row["error_id"],
                    "execution_id": row["execution_id"],
                    "timestamp": row["timestamp"],
                    "component": row["component"],
                    "stage": row["stage"],
                    "severity": row["severity"],
                    "error_type": row["error_type"],
                    "message": row["message"],
                    "recoverable": bool(row["recoverable"]),
                    "metadata": _load_json(row["metadata_json"]),
                }
            )
            for row in rows
        ]

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        with self.store.connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM execution_errors
                WHERE execution_id = ?
                """,
                (execution_id,),
            )

            return cursor.rowcount


class SQLiteObservabilityRepository(ObservabilityRepository):
    """Aggregate repository backed by SQLite."""

    def __init__(
        self,
        store: Optional[SQLiteObservabilityStore] = None,
        *,
        database_path: str = "data/observability.db",
    ) -> None:
        self.store = store or SQLiteObservabilityStore(
            database_path=database_path,
        )

        self.traces = SQLiteTraceRepository(self.store)

        self.events = SQLiteEventRepository(self.store)

        self.metrics = SQLiteMetricsRepository(self.store)

        self.errors = SQLiteErrorRepository(self.store)

    def save_trace(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionTrace:
        """
        Persist a complete trace atomically.

        Child records are synchronized using immutable identifiers.
        """
        with self.store.connection() as connection:
            connection.execute(
                """
                INSERT INTO execution_traces (
                    execution_id,
                    status,
                    started_at,
                    finished_at,
                    context_json,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(execution_id)
                DO UPDATE SET
                    status = excluded.status,
                    started_at = excluded.started_at,
                    finished_at = excluded.finished_at,
                    context_json = excluded.context_json,
                    metadata_json = excluded.metadata_json
                """,
                (
                    trace.execution_id,
                    trace.status.value,
                    (
                        trace.started_at.isoformat()
                        if trace.started_at is not None
                        else None
                    ),
                    (
                        trace.finished_at.isoformat()
                        if trace.finished_at is not None
                        else None
                    ),
                    (
                        _json(trace.context.to_dict())
                        if trace.context is not None
                        else None
                    ),
                    _json(trace.metadata),
                ),
            )

            connection.execute(
                """
                DELETE FROM execution_states
                WHERE execution_id = ?
                """,
                (trace.execution_id,),
            )

            connection.execute(
                """
                DELETE FROM execution_events
                WHERE execution_id = ?
                """,
                (trace.execution_id,),
            )

            connection.execute(
                """
                DELETE FROM execution_metrics
                WHERE execution_id = ?
                """,
                (trace.execution_id,),
            )

            connection.execute(
                """
                DELETE FROM execution_errors
                WHERE execution_id = ?
                """,
                (trace.execution_id,),
            )

            for state in trace.state_history:
                connection.execute(
                    """
                    INSERT INTO execution_states (
                        execution_id,
                        status,
                        current_component,
                        current_stage,
                        current_step,
                        started_at,
                        updated_at,
                        metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        state.execution_id,
                        state.status.value,
                        state.current_component,
                        state.current_stage,
                        state.current_step,
                        (state.started_at.isoformat() if state.started_at else None),
                        state.updated_at.isoformat(),
                        _json(state.metadata),
                    ),
                )

            for event in trace.events:
                connection.execute(
                    """
                    INSERT INTO execution_events (
                        event_id,
                        execution_id,
                        event_type,
                        timestamp,
                        component,
                        stage,
                        status,
                        metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.event_id,
                        event.execution_id,
                        event.event_type.value,
                        event.timestamp.isoformat(),
                        event.component,
                        event.stage,
                        (event.status.value if event.status else None),
                        _json(event.metadata),
                    ),
                )

            for metric in trace.metrics:
                connection.execute(
                    """
                    INSERT INTO execution_metrics (
                        execution_id,
                        metric_name,
                        value,
                        unit,
                        timestamp,
                        component,
                        metric_type,
                        metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        metric.execution_id,
                        metric.metric_name,
                        metric.value,
                        metric.unit,
                        metric.timestamp.isoformat(),
                        metric.component,
                        metric.metric_type.value,
                        _json(metric.metadata),
                    ),
                )

            for error in trace.errors:
                connection.execute(
                    """
                    INSERT INTO execution_errors (
                        error_id,
                        execution_id,
                        timestamp,
                        component,
                        stage,
                        severity,
                        error_type,
                        message,
                        recoverable,
                        metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        error.error_id,
                        error.execution_id,
                        error.timestamp.isoformat(),
                        error.component,
                        error.stage,
                        error.severity.value,
                        error.error_type,
                        error.message,
                        int(error.recoverable),
                        _json(error.metadata),
                    ),
                )

        return deepcopy(trace)

    def get_trace(
        self,
        execution_id: str,
    ) -> Optional[ExecutionTrace]:
        """Reconstruct a complete trace from SQLite."""
        trace = self.traces.get(execution_id)

        if trace is None:
            return None

        trace.events = self.events.get_by_execution_id(execution_id)

        trace.metrics = self.metrics.get_by_execution_id(execution_id)

        trace.errors = self.errors.get_by_execution_id(execution_id)

        trace.state_history = self._states(
            execution_id,
        )

        if trace.state_history:
            trace.state = deepcopy(trace.state_history[-1])

        return trace

    def list_traces(
        self,
        *,
        limit: Optional[int] = None,
    ) -> List[ExecutionTrace]:
        """Return complete execution history."""
        traces = self.traces.list(
            limit=limit,
        )

        result = []

        for trace in traces:
            reconstructed = self.get_trace(trace.execution_id)

            if reconstructed is not None:
                result.append(reconstructed)

        return result

    def exists(
        self,
        execution_id: str,
    ) -> bool:
        """Return whether a trace exists."""
        return self.traces.get(execution_id) is not None

    def delete_trace(
        self,
        execution_id: str,
    ) -> bool:
        """Delete complete trace and children."""
        return self.traces.delete(execution_id)

    def _states(
        self,
        execution_id: str,
    ) -> List[ExecutionState]:
        with self.store.connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM execution_states
                WHERE execution_id = ?
                ORDER BY updated_at ASC, id ASC
                """,
                (execution_id,),
            ).fetchall()

        return [
            ExecutionState.from_dict(
                {
                    "execution_id": row["execution_id"],
                    "status": row["status"],
                    "current_component": row["current_component"],
                    "current_stage": row["current_stage"],
                    "current_step": row["current_step"],
                    "started_at": row["started_at"],
                    "updated_at": row["updated_at"],
                    "metadata": _load_json(row["metadata_json"]),
                }
            )
            for row in rows
        ]
