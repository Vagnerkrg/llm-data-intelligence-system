"""SQLite storage engine for Observability."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional


class SQLiteObservabilityStore:
    """Manage SQLite connections and schema."""

    def __init__(
        self,
        database_path: str = "data/observability.db",
    ) -> None:
        self.database_path = Path(database_path)

        self._memory_connection: Optional[sqlite3.Connection] = None

        if database_path == ":memory:":
            self._memory_connection = sqlite3.connect(
                ":memory:",
            )

            self._memory_connection.row_factory = sqlite3.Row

            self._configure_connection(
                self._memory_connection,
            )

            self.initialize()

            return

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a transactional SQLite connection."""

        if self._memory_connection is not None:
            connection = self._memory_connection

            try:
                yield connection
                connection.commit()

            except Exception:
                connection.rollback()
                raise

            return

        connection = sqlite3.connect(
            str(self.database_path),
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        connection.row_factory = sqlite3.Row

        self._configure_connection(
            connection,
        )

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def initialize(self) -> None:
        """Create the Observability schema."""

        with self.connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS execution_traces (
                    execution_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT,
                    context_json TEXT,
                    metadata_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS execution_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_component TEXT,
                    current_stage TEXT,
                    current_step TEXT,
                    started_at TEXT,
                    updated_at TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    UNIQUE (
                        execution_id,
                        updated_at,
                        status,
                        current_component,
                        current_stage,
                        current_step
                    ),
                    FOREIGN KEY (
                        execution_id
                    )
                    REFERENCES execution_traces(
                        execution_id
                    )
                    ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS execution_events (
                    event_id TEXT PRIMARY KEY,
                    execution_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    component TEXT NOT NULL,
                    stage TEXT,
                    status TEXT,
                    metadata_json TEXT NOT NULL,
                    FOREIGN KEY (
                        execution_id
                    )
                    REFERENCES execution_traces(
                        execution_id
                    )
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_events_execution_id
                ON execution_events(execution_id);

                CREATE INDEX IF NOT EXISTS idx_events_timestamp
                ON execution_events(timestamp);

                CREATE TABLE IF NOT EXISTS execution_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    component TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    FOREIGN KEY (
                        execution_id
                    )
                    REFERENCES execution_traces(
                        execution_id
                    )
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_metrics_execution_id
                ON execution_metrics(execution_id);

                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp
                ON execution_metrics(timestamp);

                CREATE TABLE IF NOT EXISTS execution_errors (
                    error_id TEXT PRIMARY KEY,
                    execution_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    component TEXT NOT NULL,
                    stage TEXT,
                    severity TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    recoverable INTEGER NOT NULL,
                    metadata_json TEXT NOT NULL,
                    FOREIGN KEY (
                        execution_id
                    )
                    REFERENCES execution_traces(
                        execution_id
                    )
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_errors_execution_id
                ON execution_errors(execution_id);

                CREATE INDEX IF NOT EXISTS idx_errors_timestamp
                ON execution_errors(timestamp);
                """
            )

    @staticmethod
    def _configure_connection(
        connection: sqlite3.Connection,
    ) -> None:
        """Configure SQLite connection defaults."""

        connection.execute("PRAGMA foreign_keys = ON")

    @staticmethod
    def normalize_database_path(
        database_path: Optional[str],
    ) -> str:
        """Return a usable database path."""

        return database_path or "data/observability.db"

    def close(self) -> None:
        """Close the persistent in-memory connection."""

        if self._memory_connection is not None:
            self._memory_connection.close()
            self._memory_connection = None
