from ..domain.evaluation_context import EvaluationContext
from ..domain.evaluation_finding import EvaluationFinding


class QualityAnalyzer:
    """
    Analyzes execution quality based on evaluation context.
    """

    def analyze(
        self,
        context: EvaluationContext,
    ) -> list[EvaluationFinding]:
        """
        Generate quality findings.

        Initial implementation provides
        deterministic rule-based analysis.
        """

        findings: list[EvaluationFinding] = []

        if len(context.tools_used) > 5:
            findings.append(
                EvaluationFinding(
                    category="tool_usage",
                    severity="medium",
                    description=(
                        "Execution used a high number of tools."
                    ),
                )
            )

        return findings