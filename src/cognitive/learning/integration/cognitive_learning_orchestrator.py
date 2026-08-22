from typing import Dict, Any

from src.cognitive.learning.patterns.pattern_detector import PatternDetector

from src.cognitive.learning.consolidation.consolidation_engine import (
    ConsolidationEngine,
)

from src.cognitive.learning.knowledge.knowledge_store import KnowledgeStore


class CognitiveLearningOrchestrator:
    """
    Orchestrates the cognitive learning lifecycle.

    Flow:

    Feedback
        |
        v
    Pattern Detection
        |
        v
    Pattern Reinforcement
        |
        v
    Knowledge Consolidation
        |
        v
    Persistent Memory
    """

    def __init__(
        self,
        pattern_detector: PatternDetector,
        consolidation_engine: ConsolidationEngine,
        knowledge_store: KnowledgeStore,
    ):

        self.pattern_detector = pattern_detector
        self.consolidation_engine = consolidation_engine
        self.knowledge_store = knowledge_store

    def process_learning(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process feedback and transform it into reusable knowledge.
        """

        pattern = self.pattern_detector.detect(
            feedback.get("type"), feedback.get("description"), metadata=feedback
        )

        confidence = feedback.get("confidence", 0)

        impact = feedback.get("impact", "low")

        if confidence >= 0.8 and impact == "high":
            pattern.strengthen(0.3)

        if pattern.frequency > 1:
            pattern.strengthen(0.05)

        knowledge = self.consolidation_engine.consolidate(pattern)

        if knowledge is None:
            return {"learned": False, "reason": "Pattern not reliable enough"}

        return {
            "learned": True,
            "knowledge_id": knowledge.knowledge_id,
            "source_pattern": knowledge.source_pattern,
        }
