from src.agents.planning.adaptive_replanning_policy import (
    AdaptiveReplanningPolicy
)



def test_policy_keeps_execution_when_everything_is_normal():

    policy = AdaptiveReplanningPolicy()


    decision = policy.evaluate(
        execution_state={
            "status": "running"
        },
        feedback={
            "requires_adjustment": False
        },
        evaluation={
            "failed": False
        }
    )


    assert decision.should_replan is False

    assert decision.strategy == "continue"



def test_policy_replans_after_failure():

    policy = AdaptiveReplanningPolicy()


    decision = policy.evaluate(
        execution_state={
            "status": "running"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert decision.should_replan is True

    assert decision.reason == "execution_failure_detected"

    assert decision.strategy == "recovery"



def test_policy_replans_when_feedback_requests_adjustment():

    policy = AdaptiveReplanningPolicy()


    decision = policy.evaluate(
        execution_state={},
        feedback={
            "requires_adjustment": True
        },
        evaluation={
            "failed": False
        }
    )


    assert decision.should_replan is True

    assert decision.strategy == "adaptation"



def test_policy_replans_when_execution_is_blocked():

    policy = AdaptiveReplanningPolicy()


    decision = policy.evaluate(
        execution_state={
            "blocked": True
        },
        feedback={},
        evaluation={}
    )


    assert decision.should_replan is True

    assert decision.strategy == "alternative_path"