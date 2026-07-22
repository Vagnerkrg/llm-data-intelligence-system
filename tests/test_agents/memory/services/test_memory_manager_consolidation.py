from src.agents.memory.services.memory_manager import (
    MemoryManager
)

from src.agents.memory.services.memory_writer import (
    MemoryWriter
)

from src.agents.memory.services.memory_retriever import (
    MemoryRetriever
)

from src.agents.memory.services.memory_validator import (
    MemoryValidator
)

from src.agents.memory.services.memory_ranker import (
    MemoryRanker
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



class FakeStore:

    def __init__(self):

        self.memory = None


    def save(
        self,
        memory
    ):

        self.memory = memory



    def get(
        self,
        memory_id
    ):

        return self.memory



def create_manager():

    store = FakeStore()


    return MemoryManager(
        writer=MemoryWriter(store),
        retriever=MemoryRetriever(store),
        validator=MemoryValidator(),
        ranker=MemoryRanker()
    )



def test_should_consolidate_memory():

    manager = create_manager()


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = manager.consolidate(
        memory
    )


    assert result.consolidated is True

    assert result.memory_id == "001"



def test_should_fail_consolidation_with_invalid_memory():

    manager = create_manager()


    result = manager.consolidate(
        None
    )


    assert result.consolidated is False