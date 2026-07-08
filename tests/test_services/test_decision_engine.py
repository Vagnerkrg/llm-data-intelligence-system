from src.services.decision_engine import DecisionEngine



class TestDecisionEngine:
    """
    Tests for DecisionEngine service.
    """



    def setup_method(self):
        """
        Creates a fresh decision engine instance.
        """

        self.engine = DecisionEngine()



    def test_decide_analysis_when_analysis_exists(self):
        """
        Should prioritize structured analysis results.
        """

        analysis = {
            "operation": "count_rows",
            "dataset": "products",
            "result": 32951
        }


        rag = {
            "answer": "Existem produtos cadastrados."
        }


        response = self.engine.decide(
            rag,
            analysis
        )


        assert response["type"] == "analysis"

        assert (
            response["answer"]
            ==
            analysis
        )



    def test_decide_rag_when_analysis_is_unknown(self):
        """
        Should fallback to RAG when analysis
        cannot answer the question.
        """

        analysis = {
            "operation": "unknown"
        }


        rag = {
            "answer": "Existem produtos cadastrados."
        }


        response = self.engine.decide(
            rag,
            analysis
        )


        assert response["type"] == "rag"

        assert (
            response["answer"]
            ==
            rag
        )



    def test_decide_rag_when_analysis_is_empty(self):
        """
        Should use RAG when no analysis exists.
        """

        analysis = None


        rag = {
            "answer": "Informação encontrada."
        }


        response = self.engine.decide(
            rag,
            analysis
        )


        assert response["type"] == "rag"

        assert (
            response["answer"]
            ==
            rag
        )



    def test_decide_empty_when_no_information_exists(self):
        """
        Should handle missing information safely.
        """

        response = self.engine.decide(
            None,
            None
        )


        assert response["type"] == "unknown"