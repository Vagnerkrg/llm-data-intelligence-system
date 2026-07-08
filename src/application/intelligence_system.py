from src.services.hybrid_query_engine import HybridQueryEngine
from src.services.decision_engine import DecisionEngine
from src.services.answer_generator import AnswerGenerator
from src.logging import AppLogger
from src.monitoring.metrics_tracker import MetricsTracker
from src.core.interfaces.response import IntelligenceResponse


class IntelligenceSystem:
    """
    Main application layer.

    Central orchestration layer of the
    LLM Data Intelligence System.

    Responsible for:

    - receiving user questions
    - executing hybrid intelligence
    - deciding the best source
    - generating final answers
    """


    def __init__(
        self
    ):

        self.engine = HybridQueryEngine()

        self.decision_engine = DecisionEngine()

        self.answer_generator = AnswerGenerator()


        self.logger = AppLogger(
            self.__class__.__name__
        )


        self.metrics = MetricsTracker()



    def ask(
        self,
        question: str
    ):


        self.metrics.start_timer()


        self.logger.info(
            f"[QUESTION] {question}"
        )


        result = self.engine.query(
            question
        )


        route = result.get(
            "route"
        )


        self.logger.info(
            f"[ROUTE] {route}"
        )


        internal_result = result.get(
            "result"
        )



        # -------------------------
        # Direct analysis response
        # -------------------------

        if isinstance(
            internal_result,
            dict
        ):

            if internal_result.get(
                "type"
            ) == "analysis":


                self.logger.info(
                    "[ANALYSIS] Response generated."
                )


                self.metrics.record(
                    route=route
                )


                return IntelligenceResponse(

                    answer=self.answer_generator.generate(
                        internal_result.get(
                            "answer"
                        )
                    ),

                    source="analysis",

                    confidence=1.0,

                    metadata={
                        "route": route
                    }

                )



            if internal_result.get(
                "type"
            ) == "rag":


                answer = internal_result.get(
                    "answer"
                )


                self.logger.info(
                    "[RAG] Response generated."
                )


                self.metrics.record(
                    route=route
                )


                return IntelligenceResponse(

                    answer=answer.get(
                        "answer",
                        "Resposta não encontrada."
                    ),

                    source="rag",

                    metadata={
                        "route": route
                    }

                )



        # -------------------------
        # Hybrid structure
        # -------------------------

        if route == "hybrid":


            hybrid_result = internal_result


            rag_result = hybrid_result.get(
                "rag"
            )


            analysis_result = hybrid_result.get(
                "analysis"
            )


            decision = self.decision_engine.decide(
                rag_result,
                analysis_result
            )


            answer = decision.get(
                "answer"
            )


            self.metrics.record(
                route=route
            )



            if decision.get(
                "type"
            ) == "analysis":


                self.logger.info(
                    "[HYBRID] Analysis response generated."
                )


                return IntelligenceResponse(

                    answer=self.answer_generator.generate(
                        answer
                    ),

                    source="hybrid",

                    confidence=decision.get(
                        "confidence"
                    ),

                    metadata={

                        "route": route,

                        "decision_type": "analysis"

                    }

                )



            if isinstance(
                answer,
                dict
            ):

                self.logger.info(
                    "[HYBRID] Dictionary response generated."
                )


                return IntelligenceResponse(

                    answer=answer.get(
                        "answer",
                        "Resposta não encontrada."
                    ),

                    source="hybrid",

                    metadata={

                        "route": route,

                        "decision_type": "rag"

                    }

                )



            self.logger.info(
                "[HYBRID] Response generated."
            )


            return IntelligenceResponse(

                answer=str(answer),

                source="hybrid",

                metadata={

                    "route": route,

                    "decision_type": "direct"

                }

            )



        # -------------------------
        # Error response
        # -------------------------

        self.logger.error(
            "[SYSTEM] Unable to process question."
        )


        self.metrics.record(
            route="unknown",
            status="error",
            error="Unable to process question"
        )


        return IntelligenceResponse(

            answer=
                "Não foi possível processar a pergunta.",

            source="error",

            metadata={

                "route": "unknown",

                "status": "error"

            }

        )