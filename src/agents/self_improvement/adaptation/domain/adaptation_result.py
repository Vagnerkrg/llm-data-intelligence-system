import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .adaptation_action import AdaptationAction


@dataclass
class AdaptationResult:
    """
    Result generated after applying an adaptation.
    """

    success: bool

    action: AdaptationAction

    message: str

    adaptation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))