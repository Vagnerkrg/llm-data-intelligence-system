from src.analysis.analysis_router import AnalysisRouter
from src.agents.data_analysis_agent import DataAnalysisAgent
from src.rag.query_engine import RAGQueryEngine
from src.services.decision_engine import DecisionEngine
from src.logging import AppLogger



class HybridQueryEngine:
    """
    Hybrid intelligence engine.

    Orchestrates:

    - RAG Engine
    - Data Analysis Agent
    - Decision Engine

    Responsible for selecting
    the best response strategy.
    """


    def __init__(
        self,
        analysis_router=None,
        rag_engine=None,
        analysis_agent=None,
        decision_engine=None
    ):


        self.analysis_router = (
            analysis_router
            if analysis_router
            else AnalysisRouter()
        )


        self.rag_engine = (
            rag_engine
            if rag_engine
            else RAGQueryEngine()
        )


        self.analysis_agent = (
            analysis_agent
            if analysis_agent
            else DataAnalysisAgent()
        )


        self.decision_engine = (
            decision_engine
            if decision_engine
            else DecisionEngine()
        )


        self.logger = AppLogger(
            self.__class__.__name__
        )



    def query(
        self,
        question: str
    ):


        self.logger.info(
            f"[HYBRID_QUERY] Question received: {question}"
        )


        route = self.analysis_router.route(
            question
        )


        route_type = route.get(
            "type"
        )


        self.logger.info(
            f"[HYBRID_QUERY] Route selected: {route_type}"
        )



        if route_type == "rag":

            self.logger.info(
                "[HYBRID_QUERY] Executing RAG pipeline."
            )


            rag_result = self.rag_engine.query(
                question
            )


            return {

                "route": "rag",

                "result": self.decision_engine.decide(
                    rag_result,
                    None
                )

            }



        if route_type == "analysis":

            self.logger.info(
                "[HYBRID_QUERY] Executing analysis pipeline."
            )


            analysis_result = self.analysis_agent.run(
                question
            )


            return {

                "route": "analysis",

                "result": self.decision_engine.decide(
                    None,
                    analysis_result
                )

            }



        if route_type == "hybrid":


            self.logger.info(
                "[HYBRID_QUERY] Executing hybrid pipeline."
            )


            rag_result = self.rag_engine.query(
                question
            )


            analysis_result = self.analysis_agent.run(
                question
            )


            decision = self.decision_engine.decide(
                rag_result,
                analysis_result
            )


            self.logger.info(
                "[HYBRID_QUERY] Decision generated."
            )


            return {

                "route": "hybrid",

                "result": decision

            }



        self.logger.warning(
            "[HYBRID_QUERY] Unknown route."
        )


        return {

            "route": "unknown",

            "result": {

                "type": "unknown",

                "answer": "Não foi possível processar a pergunta."

            }

        }