from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex
from src.llm.groq_client import GroqClient
from src.rag.prompt_templates import RAGPromptTemplate
from src.query.query_router import QueryRouter
from src.evaluation.rag_metrics import RAGMetrics
from src.evaluation.metrics_logger import MetricsLogger


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
    Metrics Evaluation
        |
        v
    Metrics Logging
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

        self.metrics = (
            RAGMetrics()
        )

        self.metrics_logger = (
            MetricsLogger()
        )


    def retrieve(
        self,
        question,
        top_k=3,
        min_score=0.40
    ):

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


        fallback_used = False


        if results:

            best_score = results[0]["score"]


            if best_score < min_score:

                results = self.vector_index.search(
                    embedding,
                    top_k=top_k
                )

                fallback_used = True


        return results, route, fallback_used



    def build_context(
        self,
        results
    ):
        """
        Builds structured context for the LLM.

        Adds metadata and similarity scores
        to improve context interpretation.
        """

        contexts = []


        for index, item in enumerate(
            results,
            start=1
        ):

            metadata = item.get(
                "metadata",
                {}
            )


            source = metadata.get(
                "source",
                "unknown"
            )


            doc_type = metadata.get(
                "type",
                "unknown"
            )


            score = item.get(
                "score",
                0
            )


            contexts.append(
                f"""
Document {index}

Source:
{source}

Type:
{doc_type}

Similarity Score:
{score:.4f}

Content:
{item["document"]}
"""
            )


        return "\n\n".join(
            contexts
        )



    def query(
        self,
        question,
        top_k=3
    ):

        results, route, fallback_used = self.retrieve(
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


        metrics = self.metrics.evaluate(
            question,
            route,
            results,
            fallback_used
        )


        self.metrics_logger.log(
            metrics
        )


        return {

            "answer": answer,

            "route": route,

            "sources": results,

            "metrics": metrics

        }