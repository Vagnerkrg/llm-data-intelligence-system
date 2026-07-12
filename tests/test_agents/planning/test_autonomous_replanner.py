from src.agents.planning.autonomous_replanner import (
    AutonomousReplanner,
)

from src.agents.planning.execution_plan import (
    ExecutionPlan,
)

from src.agents.planning.plan_step import (
    PlanStep,
)

from src.agents.planning.replanning_decision import (
    ReplanningDecision,
)


def create_sample_plan():
    """
    Creates a basic execution plan.
    """

    return ExecutionPlan(
        objective="Analyze data",
        steps=[
            PlanStep(
                step_id=1,
                action="analyze",
                description="Initial analysis step",
            )
        ]
    )


def test_replanner_keeps_plan_when_no_replanning():
    """
    Validate no modification without replanning.
    """

    replanner = AutonomousReplanner()

    plan = create_sample_plan()

    decision = ReplanningDecision(
        should_replan=False,
        reason="Execution completed successfully",
    )

    updated_plan = replanner.replan(
        plan,
        decision,
    )

    assert len(updated_plan.steps) == 1



def test_replanner_adds_recovery_step():
    """
    Validate adaptive recovery step creation.
    """

    replanner = AutonomousReplanner()

    plan = create_sample_plan()

    decision = ReplanningDecision(
        should_replan=True,
        reason="Execution failure detected",
        issues=[
            "Tool timeout"
        ],
    )

    updated_plan = replanner.replan(
        plan,
        decision,
    )


    assert len(updated_plan.steps) == 2

    assert (
        updated_plan.steps[-1].action
        == "adaptive_recovery"
    )



def test_replanner_preserves_original_plan():
    """
    Validate immutable replanning behavior.
    """

    replanner = AutonomousReplanner()

    plan = create_sample_plan()

    decision = ReplanningDecision(
        should_replan=True,
        reason="Failure",
    )

    updated_plan = replanner.replan(
        plan,
        decision,
    )


    assert len(plan.steps) == 1

    assert len(updated_plan.steps) == 2



def test_replanner_creates_metadata():
    """
    Validate adaptive step metadata.
    """

    replanner = AutonomousReplanner()

    plan = create_sample_plan()

    decision = ReplanningDecision(
        should_replan=True,
        reason="Need adaptation",
        issues=[
            "Timeout"
        ],
    )


    updated_plan = replanner.replan(
        plan,
        decision,
    )


    step = updated_plan.steps[-1]


    assert (
        step.metadata["reason"]
        == "Need adaptation"
    )

    assert (
        "Timeout"
        in step.metadata["issues"]
    )