from src.agents.runtime.observed_execution_runtime import (
    ObservedExecutionRuntime
)

from src.agents.planning.execution_plan import (
    ExecutionPlan
)



def test_observed_runtime_returns_observation():

    runtime = ObservedExecutionRuntime()


    result = runtime.run_cycle(
        plan=ExecutionPlan(
            objective="Analyze data"
        ),
        execution_state={
            "status": "running"
        },
        feedback={},
        evaluation={}
    )


    assert (
        result["observation"]["status"]
        ==
        "running"
    )



def test_observed_runtime_keeps_monitor_history():

    runtime = ObservedExecutionRuntime()


    plan = ExecutionPlan(
        objective="Generate report"
    )


    runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "running"
        },
        feedback={},
        evaluation={}
    )


    runtime.run_cycle(
        plan=plan,
        execution_state={
            "status": "completed"
        },
        feedback={},
        evaluation={}
    )


    assert (
        runtime.monitor.total_cycles()
        ==
        2
    )



def test_observed_runtime_supports_failure_detection():

    runtime = ObservedExecutionRuntime()


    result = runtime.run_cycle(
        plan=ExecutionPlan(
            objective="Analyze data"
        ),
        execution_state={
            "status": "failed"
        },
        feedback={
            "error": "execution failure"
        },
        evaluation={
            "failed": True
        }
    )


    assert (
        result["replanned"]
        is True
    )



def test_observed_runtime_returns_decision():

    runtime = ObservedExecutionRuntime()


    result = runtime.run_cycle(
        plan=ExecutionPlan(
            objective="Analysis"
        ),
        execution_state={
            "status": "failed"
        },
        feedback={},
        evaluation={
            "failed": True
        }
    )


    assert (
        result["decision"]
        is not None
    )