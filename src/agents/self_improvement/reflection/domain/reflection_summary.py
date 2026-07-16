"""Reflection summary domain model."""

from dataclasses import dataclass, field

from .reflection_finding import ReflectionFinding


@dataclass(slots=True)
class ReflectionSummary:
    """Represents the consolidated reflection result."""

    findings: list[ReflectionFinding] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    conclusion: str = ""
    confidence: float = 0.0

    @property
    def total_findings(self) -> int:
        """Return the number of findings."""
        return len(self.findings)

    @property
    def has_findings(self) -> bool:
        """Return True when findings exist."""
        return bool(self.findings)