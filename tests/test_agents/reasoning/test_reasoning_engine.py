from src.agents.reasoning.reasoning_engine import ReasoningEngine
from src.agents.reasoning.reasoning_result import ReasoningResult



def test_reasoning_engine_creation():

    engine = ReasoningEngine()


    assert engine is not None



def test_reasoning_engine_reason():

    engine = ReasoningEngine()


    result = engine.reason(

        "How many customers exist?"

    )


    assert isinstance(

        result,

        ReasoningResult

    )



def test_reasoning_engine_generates_reasoning():

    engine = ReasoningEngine()


    result = engine.reason(

        "Analyze sales data."

    )


    assert result.reasoning is not None

    assert result.conclusion is not None



def test_reasoning_engine_metadata():

    engine = ReasoningEngine()


    result = engine.reason(

        "Test request."

    )


    assert isinstance(

        result.metadata,

        dict

    )