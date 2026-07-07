from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex
from src.llm.groq_client import GroqClient


class RAGQueryEngine:
    """
    Retrieval Augmented Generation query engine.

    Connects:
    - Embeddings
    - Vector Search
    - LLM Generation
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


    def retrieve(
        self,
        question,
        top_k=3
    ):
        """
        Retrieves relevant documents.
        """

        embedding = (
            self.embedding_generator
            .generate([question])[0]
        )

        results = self.vector_index.search(
            embedding,
            top_k=top_k
        )

        return results


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

        results = self.retrieve(
            question,
            top_k
        )

        context = self.build_context(
            results
        )


        prompt = f"""
Answer the question using the context below.

Context:
{context}


Question:
{question}
"""


        answer = self.llm.generate(
            prompt
        )


        return {
            "answer": answer,
            "sources": results
        }