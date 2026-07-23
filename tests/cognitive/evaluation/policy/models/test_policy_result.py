from src.cognitive.evaluation.policy.models.policy import (
    Policy,
)

from src.cognitive.evaluation.policy.models.policy_result import (
    PolicyResult,
)

from src.cognitive.evaluation.policy.models.policy_type import (
    PolicyType,
)


def test_policy_result():

    result = PolicyResult(

        policy=Policy(

            policy_type=PolicyType.AUTOMATIC

        ),

        accepted=True,

        reason="Score accepted",

    )

    assert result.approved()

    assert result.reason == "Score accepted"