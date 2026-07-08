from src.application.intelligence_system import IntelligenceSystem
from src.core.interfaces.response import IntelligenceResponse



class FakeEngine:


    def __init__(
        self,
        result
    ):

        self.result = result



    def query(
        self,
        question
    ):

        return self.result





class FakeAnswerGenerator:


    def generate(
        self,
        result
    ):

        return "analysis response"





class TestIntelligenceSystem:



    def test_analysis_response(self):


        system = IntelligenceSystem()


        system.engine = FakeEngine(

            {
                "route":"analysis",

                "result":{

                    "type":"analysis",

                    "answer":{

                        "operation":"count_rows"

                    }

                }

            }

        )


        system.answer_generator = FakeAnswerGenerator()



        result = system.ask(

            "Quantos produtos existem?"

        )



        assert isinstance(

            result,

            IntelligenceResponse

        )


        assert result.answer == (

            "analysis response"

        )


        assert result.source == (

            "analysis"

        )


        assert "request_id" in result.metadata



    def test_rag_response(self):


        system = IntelligenceSystem()



        system.engine = FakeEngine(

            {

                "route":"rag",

                "result":{

                    "type":"rag",

                    "answer":{

                        "answer":"rag response"

                    }

                }

            }

        )



        result = system.ask(

            "Quais produtos aparecem?"

        )



        assert isinstance(

            result,

            IntelligenceResponse

        )


        assert result.answer == (

            "rag response"

        )


        assert result.source == (

            "rag"

        )


        assert "request_id" in result.metadata



    def test_unknown_response(self):


        system = IntelligenceSystem()



        system.engine = FakeEngine(

            {

                "route":"unknown",

                "result":{}

            }

        )



        result = system.ask(

            "???"

        )



        assert isinstance(

            result,

            IntelligenceResponse

        )


        assert result.source == (

            "system"

        )


        assert result.answer == (

            "Não foi possível processar a pergunta."

        )


        assert result.metadata["status"] == (

            "error"

        )


        assert "request_id" in result.metadata