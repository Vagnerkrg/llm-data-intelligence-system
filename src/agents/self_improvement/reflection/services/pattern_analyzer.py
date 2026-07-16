from src.agents.self_improvement.reflection.domain import (
    ReflectionFinding,
)


class PatternAnalyzer:
    """
    Detects behavioral patterns from reflection context.
    """

    def __init__(self):
        pass


    def analyze(self, context):
        """
        Analyze reflection context.

        Supports:
        - ReflectionContext
        - raw metrics list
        """

        findings = []


        if isinstance(context, list):

            if not context:
                return []


            execution_values = [
                item["value"]
                for item in context
                if item.get(
                    "metric"
                ) == "execution_time"
            ]


            if len(execution_values) >= 2:

                if execution_values[-1] < execution_values[0]:

                    findings.append(
                        ReflectionFinding(
                            title="Performance Improvement",
                            description=(
                                "Execution time decreased "
                                "over iterations."
                            ),
                            confidence=0.9,
                            reflection_type="performance",
                        )
                    )


            return findings


        if getattr(
            context,
            "has_adaptations",
            False,
        ):

            findings.append(
                ReflectionFinding(
                    title="Adaptation Pattern",
                    description=(
                        "Adaptations detected "
                        "inside reflection context."
                    ),
                    confidence=0.8,
                    reflection_type="adaptation",
                )
            )


        return findings