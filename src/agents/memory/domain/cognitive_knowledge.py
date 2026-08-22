from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class CognitiveKnowledge:
    """
    Represents reusable knowledge
    consolidated from memory patterns.
    """

    knowledge_id: str

    description: str

    source_patterns: List[str] = field(default_factory=list)

    confidence: float = 0.0

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
