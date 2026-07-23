from src.cognitive.evaluation.policy.models.policy_type import (
    PolicyType,
)


def test_policy_type_values():

    assert PolicyType.AUTOMATIC.value == "automatic"

    assert PolicyType.HUMAN_REVIEW.value == "human_review"

    assert PolicyType.SAFE_MODE.value == "safe_mode"

    assert PolicyType.REPLAN.value == "replan"

    assert PolicyType.ABORT.value == "abort"