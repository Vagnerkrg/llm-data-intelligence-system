from src.services.hybrid_query_engine import HybridQueryEngine
from src.services.decision_engine import DecisionEngine
from src.services.answer_generator import AnswerGenerator



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



    def ask(
        self,
        question: str
    ):


        result = self.engine.query(
            question
        )


        route = result.get(
            "route"
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


                return answer.get(
                    "answer",
                    "Resposta não encontrada."
                )



        # -------------------------
        # Old hybrid structure
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


            if decision.get(
                "type"
            ) == "analysis":


                return self.answer_generator.generate(
                    answer
                )


            if isinstance(
                answer,
                dict
            ):

                return answer.get(
                    "answer"
                )


            return str(answer)



        return {

            "type":"error",

            "message":
                "Não foi possível processar a pergunta."

        }