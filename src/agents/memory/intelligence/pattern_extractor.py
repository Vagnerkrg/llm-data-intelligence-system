from typing import List

from src.agents.memory.domain.memory_entry import MemoryEntry

from src.agents.memory.domain.pattern import Pattern


class PatternExtractor:
    """
    Extracts recurring patterns
    from memory experiences.
    """

    def extract(self, memories: List[MemoryEntry]) -> List[Pattern]:
        """
        Extract repeated content patterns.
        """

        if not memories:
            return []

        grouped = {}

        for memory in memories:
            key = memory.content

            if key not in grouped:
                grouped[key] = []

            grouped[key].append(memory)

        patterns = []

        for index, items in enumerate(grouped.values()):
            if len(items) < 2:
                continue

            patterns.append(
                Pattern(
                    pattern_id=f"pattern_{index}",
                    description=items[0].content,
                    occurrences=len(items),
                    memory_ids=[memory.memory_id for memory in items],
                    confidence=(min(len(items) / 10, 1.0)),
                )
            )

        return patterns
