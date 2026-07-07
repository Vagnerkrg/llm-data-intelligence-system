from abc import ABC, abstractmethod
from typing import List


class EmbeddingGenerator(ABC):
    """
    Abstract interface for embedding generation.

    All embedding providers must implement
    this contract.
    """


    @abstractmethod
    def generate(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generates vector embeddings from text inputs.

        Parameters:
            texts:
                List of text documents.

        Returns:
            List of embedding vectors.
        """

        pass