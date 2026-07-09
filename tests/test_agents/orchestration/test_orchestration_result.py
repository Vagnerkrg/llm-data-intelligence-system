from src.agents.orchestration.orchestration_result import (
    OrchestrationResult
)



def test_orchestration_result_creation():

    result = OrchestrationResult(

        status="completed",

        result={
            "answer": "ok"
        }

    )


    assert result.status == "completed"



def test_orchestration_result_to_dict():

    result = OrchestrationResult(

        status="completed",

        result="data",

        reasoning="analysis"

    )


    data = result.to_dict()


    assert data["status"] == "completed"

    assert data["result"] == "data"

    assert data["reasoning"] == "analysis"



def test_orchestration_result_metadata():

    result = OrchestrationResult(

        status="completed",

        metadata={
            "source": "test"
        }

    )


    assert (
        result.metadata["source"]
        ==
        "test"
    )