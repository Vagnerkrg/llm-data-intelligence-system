from src.agents.self_improvement.knowledge.services.knowledge_manager import (
    KnowledgeManager,
)


def test_knowledge_pipeline_flow():

    manager = KnowledgeManager()

    result = manager.process(
        {
            "source": "evaluation",
            "pattern": "execution_failure",
            "recommendation": "adjust_plan",
            "confidence": 0.85,
        }
    )

    assert result is not None
    assert result.confidence == 0.85