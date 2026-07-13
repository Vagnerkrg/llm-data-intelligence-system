from dataclasses import dataclass, field


@dataclass(slots=True)
class ReflectionResult:
    """
    Represents the cognitive analysis generated
    from an observed agent execution.

    Stores findings, interpretation and recommendations
    produced during the reflection process.
    """

    reflection_id: str
    observation_id: str

    analysis: str

    findings: list[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    recommendations: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )