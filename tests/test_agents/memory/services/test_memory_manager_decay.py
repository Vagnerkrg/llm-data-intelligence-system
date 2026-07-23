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



def test_should_apply_memory_decay():

    manager = create_manager()


    memory = MemoryEntry(
        memory_id="001",
        content="Old preference.",
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "relevance_score": 1.0
        }
    )


    result = manager.decay(
        memory
    )


    assert result["memory_id"] == "001"

    assert result["score"] < 1.0

    assert result["decayed"] is True



def test_should_fail_decay_with_invalid_memory():

    manager = create_manager()


    result = manager.decay(
        None
    )


    assert result["score"] == 0.0

    assert result["decayed"] is False