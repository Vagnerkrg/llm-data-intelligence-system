from src.application.intelligence_system import (
    IntelligenceSystem
)

from src.core.interfaces.response import (
    IntelligenceResponse
)


from tests.fixtures.sample_responses import (
    RAG_RESPONSE
)



class FakeEngine:


    def query(
        self,
        question
    ):

        return RAG_RESPONSE




def test_complete_intelligence_flow():


    system = IntelligenceSystem()



    system.engine = FakeEngine()



    response = system.ask(

        "Quais produtos aparecem?"

    )



    assert isinstance(

        response,

        IntelligenceResponse

    )



    assert response.answer == (

        "RAG test response"

    )



    assert response.source == (

        "rag"

    )