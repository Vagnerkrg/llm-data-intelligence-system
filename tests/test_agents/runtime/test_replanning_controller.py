from src.agents.runtime.replanning_controller import (
    ReplanningController
)

from src.agents.planning.execution_plan import (
    ExecutionPlan
)



def test_controller_keeps_plan_when_execution_is_normal():

    controller = ReplanningController()


    plan = ExecutionPlan(
        objective="Analyze data"
    )


    result = controller.evaluate_execution(
        plan=plan,
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


    assert result["replanned"] is False

    assert result["plan"] == plan



def test_controller_triggers_replanning_after_failure():

    controller = ReplanningController()


    plan = ExecutionPlan(
        objective="Analyze data"
    )


    result = controller.evaluate_execution(
        plan=plan,
        execution_state={
            "status": "running"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert result["replanned"] is True



def test_controller_returns_decision():

    controller = ReplanningController()


    result = controller.evaluate_execution(
        plan=ExecutionPlan(),
        execution_state={},
        feedback={},
        evaluation={}
    )


    assert result["decision"] is not None



def test_controller_contains_replanning_flow():

    controller = ReplanningController()


    assert controller.policy is not None

    assert controller.replanner is not None