"""Reflection validator service."""

from ..domain import ReflectionSummary


class ReflectionValidator:
    """Validate the quality of a reflection summary."""

    def validate(
        self,
        summary: ReflectionSummary,
    ) -> bool:
        """Return True when the reflection summary is considered valid."""

        if not summary.findings:
            return False

        if summary.confidence < 0.0:
            return False

        if summary.confidence > 1.0:
            return False

        return True