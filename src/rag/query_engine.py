from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex
from src.llm.groq_client import GroqClient
from src.rag.prompt_templates import RAGPromptTemplate
from src.query.query_router import QueryRouter



class RAGQueryEngine:
    """
    Retrieval Augmented Generation query engine.

    Pipeline:

    Question
        |
        v
    Query Router
        |
        v
    Metadata Filter
        |
        v
    Vector Search
        |
        v
    Fallback Search
        |
        v
    Prompt Template
        |
        v
    LLM
    """



    def __init__(
        self,
        vector_index_path="models/vector_index.pkl"
    ):


        self.embedding_generator = (
            LocalEmbeddingGenerator()
        )


        self.vector_index = VectorIndex(
            vector_index_path
        )


        self.vector_index.load()


        self.llm = GroqClient()


        self.prompt_template = (
            RAGPromptTemplate()
        )


        self.router = (
            QueryRouter()
        )



    def retrieve(
        self,
        question,
        top_k=3,
        min_score=0.40
    ):
        """
        Retrieves relevant documents using routing
        with fallback to global search.
        """


        route = self.router.route(
            question
        )


        embedding = (
            self.embedding_generator
            .generate([question])[0]
        )


        source = None


        if route["domain"] != "general":

            source = route["domain"]



        results = self.vector_index.search(
            embedding,
            top_k=top_k,
            source=source
        )


        if results:

            best_score = results[0]["score"]

            if best_score < min_score:

                results = self.vector_index.search(
                    embedding,
                    top_k=top_k,
                    source=None
                )


        return results, route



    def build_context(
        self,
        results
    ):
        """
        Creates context from retrieved documents.
        """


        return "\n\n".join(
            [
                item["document"]
                for item in results
            ]
        )



    def query(
        self,
        question,
        top_k=3
    ):
        """
        Executes complete RAG pipeline.
        """


        results, route = self.retrieve(
            question,
            top_k
        )


        context = self.build_context(
            results
        )


        prompt = self.prompt_template.build(
            context,
            question
        )


        answer = self.llm.generate(
            prompt
        )


        return {

            "answer": answer,

            "route": route,

            "sources": results

        }