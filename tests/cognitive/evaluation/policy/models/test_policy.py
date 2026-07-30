from src.cognitive.evaluation.policy.models.policy import (
    Policy,
)

from src.cognitive.evaluation.policy.models.policy_type import (
    PolicyType,
)


def test_policy_creation():

    policy = Policy(

        policy_type=PolicyType.AUTOMATIC,

        priority=100,

        description="Automatic approval",

    )

    assert policy.policy_type == PolicyType.AUTOMATIC

    assert policy.priority == 100

    assert policy.is_enabled()


def test_policy_can_be_disabled():

    policy = Policy(

        policy_type=PolicyType.ABORT,

        enabled=False,

    )

    assert not policy.is_enabled()