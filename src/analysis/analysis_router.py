from typing import Dict


class AnalysisRouter:
    """
    Routes user questions to the correct intelligence layer.

    Possible routes:

    - rag:
        Questions answered using document retrieval.

    - analysis:
        Questions requiring dataframe operations,
        statistics or calculations.

    - hybrid:
        Questions requiring both retrieval
        and structured analysis.
    """


    def route(
        self,
        question: str
    ) -> Dict:
        """
        Determines the required analysis strategy.
        """

        text = question.lower()


        analysis_keywords = [

            "quantos",
            "quantidade",
            "total",
            "média",
            "media",
            "soma",
            "maior",
            "menor",
            "máximo",
            "minimo",
            "mínimo",
            "percentual",
            "porcentagem",
            "estatística",
            "estatistica",
            "distribuição",
            "distribuicao"

        ]


        hybrid_keywords = [

            "qual",
            "quais",
            "melhor",
            "pior",
            "comparar",
            "relação",
            "relacao",
            "impacto"

        ]


        for keyword in analysis_keywords:

            if keyword in text:

                return {

                    "type": "analysis",

                    "confidence": 3

                }



        for keyword in hybrid_keywords:

            if keyword in text:

                return {

                    "type": "hybrid",

                    "confidence": 2

                }



        return {

            "type": "rag",

            "confidence": 1

        }