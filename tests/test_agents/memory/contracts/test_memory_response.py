from src.agents.memory.contracts.memory_response import (
    MemoryResponse
)


def test_should_create_memory_response():

    response = MemoryResponse(
        success=True,
        message="memória recuperada"
    )

    assert response.success is True

    assert response.message == (
        "memória recuperada"
    )

    assert response.memories == []


def test_should_create_memory_response_with_memories():

    response = MemoryResponse(
        success=True,
        memories=[
            {
                "id": "001",
                "content": "dados anteriores"
            }
        ]
    )

    assert len(response.memories) == 1

    assert response.memories[0]["id"] == "001"