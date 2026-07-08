from src.application.intelligence_system import IntelligenceSystem


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



class FakeDecisionEngine:


    def decide(
        self,
        rag_result,
        analysis_result
    ):

        return {

            "type":"analysis",

            "answer":analysis_result

        }



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


        system.answer_generator = (
            FakeAnswerGenerator()
        )


        result = system.ask(
            "Quantos produtos existem?"
        )


        assert (
            result
            ==
            "analysis response"
        )



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


        assert (
            result
            ==
            "rag response"
        )



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


        assert (
            result["type"]
            ==
            "error"
        )