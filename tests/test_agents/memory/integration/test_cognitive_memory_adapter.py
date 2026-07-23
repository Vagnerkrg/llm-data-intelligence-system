from src.agents.memory.integration.cognitive_memory_adapter import (
    CognitiveMemoryAdapter
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



class FakeStorage:

    def __init__(self):

        self.memory = None


    def save(
        self,
        memory
    ):

        self.memory = memory

        return memory



    def get(
        self,
        memory_id
    ):

        return self.memory



def create_adapter():

    return CognitiveMemoryAdapter(
        FakeStorage()
    )



def test_should_store_learning_memory():

    adapter = create_adapter()


    memory = MemoryEntry(
        memory_id="001",
        content="Agent learned user preference.",
        memory_type=MemoryType.LONG_TERM
    )


    result = adapter.store_learning(
        memory
    )


    assert result.memory_id == "001"



def test_should_retrieve_learning_memory():

    adapter = create_adapter()


    memory = MemoryEntry(
        memory_id="001",
        content="Previous learned knowledge.",
        memory_type=MemoryType.LONG_TERM
    )


    adapter.store_learning(
        memory
    )


    result = adapter.retrieve_learning(
        "001"
    )


    assert result.memory_id == "001"