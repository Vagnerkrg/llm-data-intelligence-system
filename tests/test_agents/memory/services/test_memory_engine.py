from src.agents.memory.services.memory_engine import (
    MemoryEngine
)

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



def create_engine():

    store = FakeStore()


    manager = MemoryManager(
        writer=MemoryWriter(store),
        retriever=MemoryRetriever(store),
        validator=MemoryValidator(),
        ranker=MemoryRanker()
    )


    return MemoryEngine(
        manager
    )



def test_should_remember_memory():

    engine = create_engine()


    memory = MemoryEntry(
        memory_id="001",
        content="Technical preference.",
        memory_type=MemoryType.LONG_TERM
    )


    result = engine.remember(
        memory
    )


    assert result.success is True



def test_should_recall_memory():

    engine = create_engine()


    memory = MemoryEntry(
        memory_id="001",
        content="Previous information.",
        memory_type=MemoryType.LONG_TERM
    )


    engine.remember(
        memory
    )


    result = engine.recall(
        "001"
    )


    assert result.success is True