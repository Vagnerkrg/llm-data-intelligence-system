from src.agents.self_improvement.reflection.domain import (
    ReflectionContext,
)


def test_should_detect_knowledge_entries():
    context = ReflectionContext(
        knowledge_entries=["knowledge"],
    )

    assert context.has_knowledge


def test_should_detect_adaptations():
    context = ReflectionContext(
        adaptation_results=["adaptation"],
    )

    assert context.has_adaptations


def test_should_detect_empty_context():
    context = ReflectionContext()

    assert not context.has_knowledge
    assert not context.has_adaptations
