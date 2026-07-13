from src.agents.runtime.autonomous_memory_runtime import (
    AutonomousMemoryRuntime
)


from src.agents.memory.autonomy_memory import (
    AutonomyMemory
)



def test_autonomous_memory_runtime_creates_memory():

    runtime = AutonomousMemoryRuntime()


    assert runtime.memory is not None



def test_autonomous_memory_runtime_stores_decision():

    runtime = AutonomousMemoryRuntime()


    decision = runtime.evaluate_and_store(
        execution_id="exec-001",
        result="Execution completed successfully",
        success=True,
    )


    assert decision is not None

    assert (
        runtime.count_memories()
        ==
        1
    )



def test_autonomous_memory_runtime_retrieves_decision():

    runtime = AutonomousMemoryRuntime()


    decision = runtime.evaluate_and_store(
        execution_id="exec-002",
        result="Execution requires adaptation",
        success=False,
    )


    stored = runtime.retrieve_learning(
        decision.decision_id
    )


    assert stored is not None

    assert (
        stored.decision_id
        ==
        decision.decision_id
    )



def test_autonomous_memory_runtime_supports_custom_memory():

    memory = AutonomyMemory()


    runtime = AutonomousMemoryRuntime(
        memory=memory
    )


    runtime.evaluate_and_store(
        execution_id="exec-003",
        result="Learning stored",
        success=True,
    )


    assert (
        memory.count()
        ==
        1
    )