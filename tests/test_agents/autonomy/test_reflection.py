from src.agents.autonomy import ReflectionResult


def test_reflection_result_creation():

    reflection = ReflectionResult(
        reflection_id="ref-001",
        observation_id="obs-001",
        analysis="Execution was successful"
    )

    assert reflection.reflection_id == "ref-001"
    assert reflection.observation_id == "obs-001"
    assert reflection.analysis == "Execution was successful"


def test_reflection_defaults():

    reflection = ReflectionResult(
        reflection_id="ref-002",
        observation_id="obs-002",
        analysis="No issues detected"
    )

    assert reflection.findings == []
    assert reflection.recommendations == []
    assert reflection.confidence == 0.0