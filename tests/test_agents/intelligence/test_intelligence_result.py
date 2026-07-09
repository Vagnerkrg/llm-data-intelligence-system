from src.agents.intelligence.intelligence_result import IntelligenceResult



def test_intelligence_result_creation():

    result = IntelligenceResult(

        answer="Final answer."

    )


    assert result.answer == "Final answer."



def test_intelligence_result_to_dict():

    result = IntelligenceResult(

        answer="Response",

        confidence=0.9

    )


    data = result.to_dict()


    assert data["answer"] == "Response"

    assert data["confidence"] == 0.9



def test_intelligence_result_metadata():

    result = IntelligenceResult(

        answer="Test",

        metadata={
            "source": "agent"
        }

    )


    assert result.metadata["source"] == "agent"