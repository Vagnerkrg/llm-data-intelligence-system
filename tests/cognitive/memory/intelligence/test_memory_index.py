from src.cognitive.memory.intelligence.memory_index import MemoryIndex


def test_memory_index_add():

    index = MemoryIndex()

    index.add("memory-001", {"type": "learning", "confidence": 0.9})

    assert index.exists("memory-001")


def test_memory_index_get():

    index = MemoryIndex()

    index.add("memory-001", {"topic": "optimization"})

    result = index.get("memory-001")

    assert result is not None
    assert result["topic"] == "optimization"


def test_memory_index_remove():

    index = MemoryIndex()

    index.add("memory-001")

    removed = index.remove("memory-001")

    assert removed is True
    assert not index.exists("memory-001")


def test_memory_index_count():

    index = MemoryIndex()

    index.add("memory-001")

    index.add("memory-002")

    assert index.count() == 2


def test_memory_index_list_ids():

    index = MemoryIndex()

    index.add("memory-001")

    ids = index.list_ids()

    assert "memory-001" in ids
