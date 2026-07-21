from src.agents.memory.domain.retrieval_result import (
    RetrievalResult
)


class MemoryRetriever:
    """
    Responsible for retrieving
    stored memories.
    """


    def __init__(
        self,
        storage
    ):
        self.storage = storage



    def retrieve(
        self,
        memory_id: str
    ) -> RetrievalResult:
        """
        Retrieve memory by identifier.
        """


        memory = self.storage.get(
            memory_id
        )


        if memory is None:

            return RetrievalResult(
                success=False,
                message=(
                    "Memory not found."
                )
            )


        return RetrievalResult(
            success=True,
            message=(
                "Memory retrieved successfully."
            ),
            memory=memory
        )