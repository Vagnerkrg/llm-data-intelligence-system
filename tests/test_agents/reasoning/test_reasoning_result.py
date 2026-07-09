from src.agents.reasoning.reasoning_result import ReasoningResult



def test_reasoning_result_creation():

    result = ReasoningResult(

        reasoning="Analyze user request.",

        conclusion="Use analytics tool."

    )


    assert result.reasoning == (
        "Analyze user request."
    )

    assert result.conclusion == (
        "Use analytics tool."
    )



def test_reasoning_result_defaults():

    result = ReasoningResult(

        reasoning="Test reasoning",

        conclusion="Test conclusion"

    )


    assert result.confidence == 0.0

    assert result.metadata == {}



def test_reasoning_result_to_dict():

    result = ReasoningResult(

        reasoning="Reasoning process",

        conclusion="Final decision",

        confidence=0.85

    )


    data = result.to_dict()


    assert data["reasoning"] == (
        "Reasoning process"
    )

    assert data["conclusion"] == (
        "Final decision"
    )

    assert data["confidence"] == 0.85