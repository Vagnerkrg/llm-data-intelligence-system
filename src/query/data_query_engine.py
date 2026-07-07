from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex
from src.query.query_router import QueryRouter



class DataQueryEngine:
    """
    Engine responsible for querying processed data.

    Uses:
    - Query routing
    - Embeddings
    - Metadata filtered vector search
    """



    def __init__(self):

        self.embedding_generator = (
            LocalEmbeddingGenerator()
        )

        self.vector_index = (
            VectorIndex()
        )

        self.router = (
            QueryRouter()
        )



    def load_index(self):
        """
        Loads persisted vector index.
        """

        self.vector_index.load()



    def query(
        self,
        question: str,
        top_k=5
    ):
        """
        Executes intelligent retrieval.
        """


        route = self.router.route(
            question
        )


        query_embedding = (
            self.embedding_generator
            .generate([question])[0]
        )



        source = None


        if route["domain"] != "general":

            source = route["domain"]



        results = (
            self.vector_index.search(
                query_embedding,
                top_k=top_k,
                source=source
            )
        )



        return {
            "route": route,
            "results": results
        }