from src.services.hybrid_query_engine import HybridQueryEngine
from src.services.response_formatter import ResponseFormatter



class IntelligenceSystem:
    """
    Main application layer.

    Orchestrates user questions
    across analysis and RAG systems.
    """


    def __init__(
        self
    ):

        self.engine = HybridQueryEngine()

        self.formatter = ResponseFormatter()



    def ask(
        self,
        question: str
    ):

        result = self.engine.query(
            question
        )


        if result.get("route") == "analysis":

            return self.formatter.format(
                result["result"]
            )


        return result