from src.analysis.analysis_router import AnalysisRouter
from src.agents.data_analysis_agent import DataAnalysisAgent
from src.rag.query_engine import RAGQueryEngine
from src.services.decision_engine import DecisionEngine



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



    def query(
        self,
        question: str
    ):


        route = self.analysis_router.route(
            question
        )



        if route["type"] == "rag":

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



        if route["type"] == "analysis":

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



        if route["type"] == "hybrid":


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


            return {

                "route": "hybrid",

                "result": decision

            }



        return {

            "route": "unknown",

            "result": {

                "type": "unknown",

                "answer": "Não foi possível processar a pergunta."

            }

        }