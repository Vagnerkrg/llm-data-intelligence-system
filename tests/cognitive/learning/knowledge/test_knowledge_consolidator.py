from src.agents.memory.domain.pattern import Pattern

from src.agents.memory.intelligence.knowledge_consolidator import KnowledgeConsolidator


def test_knowledge_consolidator_creates_knowledge():

    patterns = [
        Pattern(
            pattern_id="pattern_001",
            description="customer payment delayed",
            occurrences=3,
            memory_ids=["mem_001", "mem_002", "mem_003"],
            confidence=0.3,
        )
    ]

    consolidator = KnowledgeConsolidator()

    result = consolidator.consolidate(patterns)

    assert len(result) == 1

    assert result[0].description == "customer payment delayed"

    assert "pattern_001" in result[0].source_patterns

    assert result[0].confidence == 0.3
