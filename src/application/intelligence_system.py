from src.services.hybrid_query_engine import HybridQueryEngine
from src.services.decision_engine import DecisionEngine
from src.services.answer_generator import AnswerGenerator
from src.logging import AppLogger
from src.monitoring.metrics_tracker import MetricsTracker



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


                return self.answer_generator.generate(
                    internal_result.get(
                        "answer"
                    )
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


                return answer.get(
                    "answer",
                    "Resposta não encontrada."
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


                return self.answer_generator.generate(
                    answer
                )



            if isinstance(
                answer,
                dict
            ):

                self.logger.info(
                    "[HYBRID] Dictionary response generated."
                )


                return answer.get(
                    "answer"
                )


            self.logger.info(
                "[HYBRID] Response generated."
            )


            return str(answer)



        self.logger.error(
            "[SYSTEM] Unable to process question."
        )


        self.metrics.record(
            route="unknown",
            status="error",
            error="Unable to process question"
        )


        return {

            "type":"error",

            "message":
                "Não foi possível processar a pergunta."

        }