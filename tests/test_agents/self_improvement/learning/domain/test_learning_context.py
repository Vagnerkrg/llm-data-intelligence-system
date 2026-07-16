from src.agents.self_improvement.learning.domain import LearningContext


def test_learning_context_creation():

    context = LearningContext(
        experiences=[],
        patterns=[]
    )

    assert context.experiences == []
    assert context.patterns == []