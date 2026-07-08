from src.services.hybrid_query_engine import HybridQueryEngine


class FakeRouter:

    def __init__(self, route_type):

        self.route_type = route_type


    def route(self, question):

        return {
            "type": self.route_type
        }


class FakeRAGEngine:

    def query(self, question):

        return {
            "type": "rag",
            "answer": "RAG answer"
        }


class FakeAnalysisAgent:

    def run(self, question):

        return {
            "type": "analysis",
            "operation": "count_rows",
            "result": 10
        }


class FakeDecisionEngine:

    def decide(self, rag_result, analysis_result):

        if rag_result and analysis_result:

            return {
                "type": "hybrid",
                "answer": analysis_result
            }


        if analysis_result:

            return analysis_result


        return rag_result


class TestHybridQueryEngine:


    def test_analysis_route(self):

        engine = HybridQueryEngine(
            analysis_router=FakeRouter("analysis"),
            rag_engine=FakeRAGEngine(),
            analysis_agent=FakeAnalysisAgent(),
            decision_engine=FakeDecisionEngine()
        )


        result = engine.query(
            "Quantos produtos existem?"
        )


        assert result["route"] == "analysis"
        assert result["result"]["type"] == "analysis"



    def test_rag_route(self):

        engine = HybridQueryEngine(
            analysis_router=FakeRouter("rag"),
            rag_engine=FakeRAGEngine(),
            analysis_agent=FakeAnalysisAgent(),
            decision_engine=FakeDecisionEngine()
        )


        result = engine.query(
            "Explique os produtos."
        )


        assert result["route"] == "rag"
        assert result["result"]["type"] == "rag"



    def test_hybrid_route(self):

        engine = HybridQueryEngine(
            analysis_router=FakeRouter("hybrid"),
            rag_engine=FakeRAGEngine(),
            analysis_agent=FakeAnalysisAgent(),
            decision_engine=FakeDecisionEngine()
        )


        result = engine.query(
            "Qual categoria possui mais produtos?"
        )


        assert result["route"] == "hybrid"
        assert result["result"]["type"] == "hybrid"



    def test_unknown_route(self):

        engine = HybridQueryEngine(
            analysis_router=FakeRouter("unknown"),
            rag_engine=FakeRAGEngine(),
            analysis_agent=FakeAnalysisAgent(),
            decision_engine=FakeDecisionEngine()
        )


        result = engine.query(
            "???"
        )


        assert result["route"] == "unknown"