from src.agents.runtime.autonomous_execution_runtime import (
    AutonomousExecutionRuntime
)

from src.agents.planning.execution_plan import ExecutionPlan

from src.agents.planning.plan_step import PlanStep



def create_failed_execution_plan():

    return ExecutionPlan(
        objective="Analyze customer data",
        steps=[
            PlanStep(
                step_id=1,
                action="analyze_data",
                description="Analyze dataset",
                status="failed",
                result={
                    "error": "tool_failure"
                }
            )
        ]
    )



def test_autonomous_replanning_flow_triggers_new_plan():

    runtime = AutonomousExecutionRuntime()


    plan = create_failed_execution_plan()


    result = runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "failed"
        },
        feedback={
            "error": "tool_failure"
        },
        evaluation={
            "failed": True
        }
    )


    assert result["replanned"] is True



def test_autonomous_runtime_returns_decision():

    runtime = AutonomousExecutionRuntime()


    plan = create_failed_execution_plan()


    result = runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "failed"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert result["decision"] is not None



def test_failed_execution_generates_updated_plan():

    runtime = AutonomousExecutionRuntime()


    plan = create_failed_execution_plan()


    result = runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "failed"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert len(
        result["plan"].steps
    ) >= 1



def test_replanning_flow_preserves_original_objective():

    runtime = AutonomousExecutionRuntime()


    plan = create_failed_execution_plan()


    result = runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "failed"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert (
        result["plan"].objective
        ==
        "Analyze customer data"
    )