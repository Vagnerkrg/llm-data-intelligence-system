from typing import List

from src.agents.memory.domain.pattern import (
    Pattern
)

from src.agents.memory.domain.cognitive_knowledge import (
    CognitiveKnowledge
)


class KnowledgeConsolidator:
    """
    Consolidates extracted patterns
    into reusable cognitive knowledge.
    """


    def consolidate(
        self,
        patterns: List[Pattern]
    ) -> List[CognitiveKnowledge]:
        """
        Convert patterns into
        cognitive knowledge.
        """

        if not patterns:
            return []


        knowledge = []


        for index, pattern in enumerate(
            patterns
        ):

            knowledge.append(
                CognitiveKnowledge(
                    knowledge_id=(
                        f"knowledge_{index}"
                    ),
                    description=(
                        pattern.description
                    ),
                    source_patterns=[
                        pattern.pattern_id
                    ],
                    confidence=(
                        pattern.confidence
                    )
                )
            )


        return knowledge