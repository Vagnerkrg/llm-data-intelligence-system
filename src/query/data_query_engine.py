from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex
from src.query.query_router import QueryRouter


class DataQueryEngine:
    """
    Engine responsible for semantic retrieval over indexed data.

    Responsibilities:
    - route the question
    - generate embeddings
    - search the vector index
    - return standardized retrieval results
    """

    def __init__(
        self,
        embedding_generator=None,
        vector_index=None,
        router=None
    ):

        self.embedding_generator = (
            embedding_generator
            if embedding_generator
            else LocalEmbeddingGenerator()
        )

        self.vector_index = (
            vector_index
            if vector_index
            else VectorIndex()
        )

        self.router = (
            router
            if router
            else QueryRouter()
        )

        self._loaded = False

    def load_index(self):
        """
        Loads the persisted vector index once.
        """

        if not self._loaded:

            self.vector_index.load()
            self._loaded = True

    def query(
        self,
        question: str,
        top_k=5
    ):
        """
        Executes semantic retrieval.
        """

        self.load_index()

        route = self.router.route(question)

        query_embedding = (
            self.embedding_generator
            .generate([question])[0]
        )

        source = None

        if route["domain"] != "general":
            source = route["domain"]

        results = self.vector_index.search(
            query_embedding,
            top_k=top_k,
            source=source
        )

        return {
            "type": "rag",
            "route": route,
            "results": results,
            "total_results": len(results)
        }