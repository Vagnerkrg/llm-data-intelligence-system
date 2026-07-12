from src.agents.runtime.autonomous_execution_runtime import (
    AutonomousExecutionRuntime
)


from src.agents.planning.execution_plan import (
    ExecutionPlan
)



def test_autonomous_runtime_keeps_plan_when_execution_is_successful():

    runtime = AutonomousExecutionRuntime()


    plan = ExecutionPlan(
        objective="Analyze customer data"
    )


    result = runtime.run_cycle(
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



def test_autonomous_runtime_replans_after_failure():

    runtime = AutonomousExecutionRuntime()


    plan = ExecutionPlan(
        objective="Analyze customer data"
    )


    result = runtime.run_cycle(
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



def test_autonomous_runtime_returns_decision():

    runtime = AutonomousExecutionRuntime()


    result = runtime.run_cycle(
        plan=ExecutionPlan(),
        execution_state={},
        feedback={},
        evaluation={}
    )


    assert result["decision"] is not None



def test_autonomous_runtime_contains_execution_loop():

    runtime = AutonomousExecutionRuntime()


    assert runtime.execution_loop is not None