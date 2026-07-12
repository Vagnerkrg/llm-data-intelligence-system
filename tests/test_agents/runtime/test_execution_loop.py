from src.agents.runtime.execution_loop import (
    ExecutionLoop
)


from src.agents.planning.execution_plan import (
    ExecutionPlan
)



def test_execution_loop_continues_when_execution_is_normal():

    loop = ExecutionLoop()


    plan = ExecutionPlan(
        objective="Analyze data"
    )


    result = loop.process(
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



def test_execution_loop_replans_after_failure():

    loop = ExecutionLoop()


    plan = ExecutionPlan(
        objective="Analyze data"
    )


    result = loop.process(
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



def test_execution_loop_returns_decision():

    loop = ExecutionLoop()


    result = loop.process(
        plan=ExecutionPlan(),
        execution_state={},
        feedback={},
        evaluation={}
    )


    assert result["decision"] is not None



def test_execution_loop_contains_controller():

    loop = ExecutionLoop()


    assert loop.replanning_controller is not None