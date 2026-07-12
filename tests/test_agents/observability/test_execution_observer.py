from src.agents.observability.execution_observer import (
    ExecutionObserver
)



def test_observer_collects_execution_state():

    observer = ExecutionObserver()


    result = observer.observe(
        execution_state={
            "status": "running"
        }
    )


    assert (
        result["status"]
        ==
        "running"
    )



def test_observer_stores_feedback():

    observer = ExecutionObserver()


    observer.observe(
        execution_state={
            "status": "completed"
        },
        feedback={
            "message": "success"
        }
    )


    result = observer.last_observation()


    assert (
        result["feedback"]["message"]
        ==
        "success"
    )



def test_observer_detects_failure():

    observer = ExecutionObserver()


    observer.observe(
        execution_state={
            "status": "failed"
        }
    )


    assert (
        observer.has_failures()
        is True
    )



def test_observer_keeps_execution_history():

    observer = ExecutionObserver()


    observer.observe(
        execution_state={
            "status": "running"
        }
    )


    observer.observe(
        execution_state={
            "status": "completed"
        }
    )


    assert (
        len(observer.events)
        ==
        2
    )