from src.agents.self_improvement.knowledge.services.knowledge_manager import (
    KnowledgeManager,
)


def test_manager_processes_learning_signal():

    manager = KnowledgeManager()

    knowledge = manager.process(
        {
            "pattern": "slow_execution",
            "recommendation": "change_strategy",
            "confidence": 0.75,
        }
    )

    assert knowledge is not None
    assert knowledge.confidence == 0.75