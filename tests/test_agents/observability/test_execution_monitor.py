from src.agents.observability.execution_monitor import (
    ExecutionMonitor
)



def test_monitor_registers_execution_cycle():

    monitor = ExecutionMonitor()


    result = monitor.monitor_cycle(
        execution_state={
            "status": "running"
        }
    )


    assert (
        result["status"]
        ==
        "running"
    )



def test_monitor_counts_cycles():

    monitor = ExecutionMonitor()


    monitor.monitor_cycle(
        execution_state={
            "status": "running"
        }
    )


    monitor.monitor_cycle(
        execution_state={
            "status": "completed"
        }
    )


    assert (
        monitor.total_cycles()
        ==
        2
    )



def test_monitor_detects_failures():

    monitor = ExecutionMonitor()


    monitor.monitor_cycle(
        execution_state={
            "status": "failed"
        }
    )


    assert (
        monitor.has_failed_cycles()
        is True
    )



def test_monitor_returns_latest_cycle():

    monitor = ExecutionMonitor()


    monitor.monitor_cycle(
        execution_state={
            "status": "running"
        }
    )


    monitor.monitor_cycle(
        execution_state={
            "status": "completed"
        }
    )


    latest = monitor.latest_cycle()


    assert (
        latest["status"]
        ==
        "completed"
    )