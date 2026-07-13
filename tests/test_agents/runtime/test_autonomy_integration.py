from src.agents.runtime.autonomous_execution_runtime import (
    AutonomousExecutionRuntime
)


from src.agents.planning.execution_plan import (
    ExecutionPlan
)


from src.agents.autonomy.decision import (
    AutonomyDecision
)



def test_runtime_generates_autonomy_feedback():

    runtime = AutonomousExecutionRuntime()


    result = runtime.run_cycle(
        plan=ExecutionPlan(
            objective="Analyze data"
        ),
        execution_state={
            "status": "completed"
        },
        feedback={},
        evaluation={
            "failed": False
        }
    )


    assert (
        result["autonomy"]
        is not None
    )


    assert isinstance(
        result["autonomy"],
        AutonomyDecision
    )



def test_runtime_contains_autonomy_engine():

    runtime = AutonomousExecutionRuntime()


    assert (
        runtime.autonomy_engine
        is not None
    )