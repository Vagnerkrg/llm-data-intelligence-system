from src.agents.autonomy import Observation


def test_observation_creation():

    observation = Observation(
        observation_id="obs-001",
        context_id="ctx-001",
        execution_id="exec-001",
        observation_type="SUCCESS",
        state="Execution completed"
    )

    assert observation.observation_id == "obs-001"
    assert observation.context_id == "ctx-001"
    assert observation.observation_type == "SUCCESS"
    assert observation.state == "Execution completed"


def test_observation_metrics_default():

    observation = Observation(
        observation_id="obs-002",
        context_id="ctx-002",
        execution_id="exec-002",
        observation_type="PERFORMANCE",
        state="Completed"
    )

    assert observation.metrics == {}
    assert observation.metadata == {}