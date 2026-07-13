from src.agents.decision.decision_pipeline import DecisionPipeline
from src.agents.decision.decision_context import DecisionContext


def test_decision_pipeline_executes_complete_flow():

    context = DecisionContext(
        goal="Optimize data analysis workflow",
        capabilities=["data_analysis"],
        available_tools=["python", "llm"]
    )

    pipeline = DecisionPipeline()

    result = pipeline.run(
        context
    )

    assert result.decision_id is not None

    assert result.confidence >= 0.0

    assert result.explanation is not None