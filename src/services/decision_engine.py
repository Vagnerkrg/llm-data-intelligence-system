from typing import Dict, Any



class DecisionEngine:
    """
    Decides the best response strategy
    combining analytical and RAG results.
    """


    def decide(
        self,
        rag_result: Dict[str, Any],
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Selects or combines the best available answer.
        """


        analysis_valid = self._is_valid_analysis(
            analysis_result
        )


        if analysis_valid:

            return {

                "type": "analysis",

                "answer": analysis_result

            }



        if rag_result:

            return {

                "type": "rag",

                "answer": rag_result

            }



        return {

            "type": "unknown",

            "answer": "Não foi possível encontrar uma resposta."

        }



    def _is_valid_analysis(
        self,
        analysis_result
    ) -> bool:
        """
        Checks if analysis returned
        a meaningful result.
        """


        if not analysis_result:

            return False



        if analysis_result.get(
            "operation"
        ) == "unknown":

            return False



        return True