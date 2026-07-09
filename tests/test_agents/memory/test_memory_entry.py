from src.agents.memory.memory_entry import MemoryEntry



def test_memory_entry_creation():

    memory = MemoryEntry(

        key="user_question",

        value="How many customers?"

    )


    assert memory.key == "user_question"

    assert memory.value == "How many customers?"



def test_memory_entry_timestamp_created():

    memory = MemoryEntry(

        key="test",

        value="data"

    )


    assert memory.created_at is not None



def test_memory_entry_to_dict():

    memory = MemoryEntry(

        key="analysis",

        value="result",

        memory_type="execution",

        metadata={
            "tool": "analytics"
        }

    )


    result = memory.to_dict()


    assert result["key"] == "analysis"

    assert result["memory_type"] == "execution"

    assert result["metadata"]["tool"] == "analytics"