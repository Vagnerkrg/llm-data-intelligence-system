from typing import Dict, List, Optional, TYPE_CHECKING, Any

from src.agents.memory.memory_entry import MemoryEntry


if TYPE_CHECKING:
    from src.agents.autonomy.learning import LearningSignal



class AutonomyMemory:
    """
    Memory layer for autonomous learning.

    Stores:

    - autonomy decisions;
    - learning signals;
    - autonomous behavior history.

    Acts as memory bridge between
    autonomy engine and runtime layers.
    """



    def __init__(
        self
    ):
        self._memory: Dict[str, MemoryEntry] = {}



    def store(
        self,
        decision
    ) -> MemoryEntry:
        """
        Store autonomy decision.

        Used by AutonomousMemoryRuntime.
        """


        entry = MemoryEntry(

            key=decision.decision_id,

            value={

                "decision_id": decision.decision_id,

                "context_id": decision.context_id,

                "strategy_id": decision.strategy_id,

                "reason": decision.reason,

                "confidence": decision.confidence

            },

            memory_type="autonomy_decision"

        )


        self._memory[
            decision.decision_id
        ] = entry


        return entry



    def store_learning(
        self,
        signal: "LearningSignal"
    ) -> MemoryEntry:
        """
        Store learning signal.

        Used by autonomy learning flow.
        """


        entry = MemoryEntry(

            key=signal.signal_id,

            value={

                "signal_id": signal.signal_id,

                "reflection_id": signal.reflection_id,

                "source": signal.source,

                "pattern": signal.pattern,

                "impact": signal.impact,

                "confidence": signal.confidence

            },

            memory_type="autonomy_learning",

            metadata={

                "source": signal.source,

                "confidence": signal.confidence

            }

        )


        self._memory[
            signal.signal_id
        ] = entry


        return entry



    def get(
        self,
        key: str
    ) -> Optional[MemoryEntry]:
        """
        Retrieve memory entry by key.
        """


        return self._memory.get(
            key
        )



    def get_learning(
        self,
        signal_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve learning signal data.
        """


        entry = self._memory.get(
            signal_id
        )


        if entry:

            return entry.value


        return None



    def list_learning(
        self
    ) -> List[MemoryEntry]:
        """
        Return stored autonomy memories.
        """


        return list(
            self._memory.values()
        )



    def count(
        self
    ) -> int:
        """
        Return number of stored memories.
        """


        return len(
            self._memory
        )



    def clear(
        self
    ):
        """
        Clear all memories.
        """


        self._memory.clear()