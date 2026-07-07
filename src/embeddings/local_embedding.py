from typing import List

from sentence_transformers import SentenceTransformer

from src.embeddings.embedding_generator import EmbeddingGenerator


class LocalEmbeddingGenerator(EmbeddingGenerator):
    """
    Local embedding implementation using Sentence Transformers.

    This component converts text documents into vector representations.
    """


    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initializes the embedding model.

        Parameters:
            model_name:
                HuggingFace sentence-transformers model.
        """

        self.model = SentenceTransformer(
            model_name
        )


    def generate(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generates embeddings from text inputs.

        Parameters:
            texts:
                List of documents.

        Returns:
            Vector embeddings.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings.tolist()