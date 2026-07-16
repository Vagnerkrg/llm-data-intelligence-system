from src.agents.self_improvement.adaptation.services.adaptation_policy import (
    AdaptationPolicy,
)


def test_adaptation_policy_allows_high_confidence():

    policy = AdaptationPolicy()

    result = policy.evaluate(0.9)

    assert result is True


def test_adaptation_policy_rejects_low_confidence():

    policy = AdaptationPolicy()

    result = policy.evaluate(0.2)

    assert result is False