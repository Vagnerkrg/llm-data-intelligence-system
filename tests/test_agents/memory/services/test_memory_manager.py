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

        if self.memory:

            return self.memory

        return None



def create_manager():

    store = FakeStore()


    return MemoryManager(
        writer=MemoryWriter(store),
        retriever=MemoryRetriever(store),
        validator=MemoryValidator(),
        ranker=MemoryRanker()
    )



def test_should_store_memory():

    manager = create_manager()


    memory = MemoryEntry(
        memory_id="001",
        content="User likes technical answers.",
        memory_type=MemoryType.LONG_TERM
    )


    result = manager.store(
        memory
    )


    assert result.success is True



def test_should_retrieve_memory():

    manager = create_manager()


    memory = MemoryEntry(
        memory_id="001",
        content="Previous preference.",
        memory_type=MemoryType.LONG_TERM
    )


    manager.store(
        memory
    )


    result = manager.retrieve(
        "001"
    )


    assert result.success is True