from src.agents.decision.alternative_generator import AlternativeGenerator
from src.agents.decision.decision_context import DecisionContext
from src.agents.decision.decision_alternative import DecisionAlternative


def test_alternative_generator_creates_alternatives():

    context = DecisionContext(
        goal="Optimize data analysis workflow",
        constraints=[],
        capabilities=["data_analysis"],
        available_tools=["python", "llm"],
        metadata={}
    )

    generator = AlternativeGenerator()

    alternatives = generator.generate(context)

    assert alternatives is not None
    assert isinstance(alternatives, list)
    assert len(alternatives) > 0

    assert isinstance(alternatives[0], DecisionAlternative)