from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime, timezone


@dataclass
class ExecutionTrace:
    """
    Represents a complete trace
    of an autonomous execution lifecycle.
    """

    execution_id: str

    events: List[Dict[str, Any]] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


    def add_event(
        self,
        event_type: str,
        payload: Dict[str, Any]
    ):
        """
        Register a new execution event.
        """

        self.events.append(
            {
                "type": event_type,
                "payload": payload,
                "timestamp": datetime.now(timezone.utc)
            }
        )


    def count_events(
        self
    ) -> int:
        """
        Return number of recorded events.
        """

        return len(
            self.events
        )


    def summary(
        self
    ) -> Dict[str, Any]:
        """
        Return execution trace summary.
        """

        return {
            "execution_id": self.execution_id,
            "events": len(self.events),
            "metadata": self.metadata
        }