from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex


class DataQueryEngine:
    """
    Engine responsible for querying processed data
    using embeddings and vector similarity search.
    """

    def __init__(self):
        self.embedding_generator = LocalEmbeddingGenerator()
        self.vector_index = VectorIndex()


    def load_index(self):
        """
        Loads persisted vector index.
        """

        self.vector_index.load()


    def query(self, question: str, top_k=5):
        """
        Searches for relevant documents based on user question.
        """

        query_embedding = self.embedding_generator.generate(
            [question]
        )[0]

        results = self.vector_index.search(
            query_embedding,
            top_k=top_k
        )

        return results