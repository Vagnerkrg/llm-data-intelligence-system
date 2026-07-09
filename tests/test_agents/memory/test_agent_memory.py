from src.agents.memory.agent_memory import AgentMemory



def test_agent_memory_store():

    memory = AgentMemory()


    entry = memory.store(

        key="question_1",

        value="customer analysis"

    )


    assert entry.key == "question_1"

    assert memory.exists(
        "question_1"
    )



def test_agent_memory_get():

    memory = AgentMemory()


    memory.store(

        key="test",

        value="information"

    )


    result = memory.get(
        "test"
    )


    assert result.value == "information"



def test_agent_memory_list():

    memory = AgentMemory()


    memory.store(

        key="one",

        value=1

    )


    memory.store(

        key="two",

        value=2

    )


    result = memory.list_memories()


    assert len(result) == 2



def test_agent_memory_search():

    memory = AgentMemory()


    memory.store(

        key="analysis",

        value="customer analytics report"

    )


    memory.store(

        key="other",

        value="system log"

    )


    result = memory.search(
        "analytics"
    )


    assert len(result) == 1

    assert result[0].key == "analysis"



def test_agent_memory_remove():

    memory = AgentMemory()


    memory.store(

        key="remove",

        value="data"

    )


    memory.remove(
        "remove"
    )


    assert not memory.exists(
        "remove"
    )



def test_agent_memory_clear():

    memory = AgentMemory()


    memory.store(

        key="a",

        value="1"

    )


    memory.clear()


    assert len(
        memory.list_memories()
    ) == 0