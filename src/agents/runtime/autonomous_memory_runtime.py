from typing import Dict, Optional


from src.agents.autonomy.autonomy_engine import (
    AutonomyEngine
)

from src.agents.autonomy.decision import (
    AutonomyDecision
)

from src.agents.memory.autonomy_memory import (
    AutonomyMemory
)



class AutonomousMemoryRuntime:
    """
    Runtime responsible for autonomous evaluation
    with persistent decision memory.

    Flow:

    Execution
        |
        v
    AutonomyEngine
        |
        v
    AutonomyDecision
        |
        v
    AutonomyMemory
    """



    def __init__(
        self,
        autonomy_engine=None,
        memory=None
    ):

        self.autonomy_engine = (
            autonomy_engine
            if autonomy_engine
            else AutonomyEngine()
        )


        self.memory = (
            memory
            if memory
            else AutonomyMemory()
        )



    def evaluate_and_store(
        self,
        execution_id: str,
        result: str,
        success: bool,
        metrics: Optional[Dict[str, float]] = None,
    ) -> AutonomyDecision:
        """
        Evaluate execution and store autonomy decision.
        """


        decision = self.autonomy_engine.evaluate_execution(
            execution_id=execution_id,
            result=result,
            success=success,
            metrics=metrics,
        )


        self.memory.store(
            decision
        )


        return decision



    def retrieve_learning(
        self,
        decision_id: str
    ) -> Optional[AutonomyDecision]:
        """
        Retrieve stored autonomy decision.
        """


        entry = self.memory.get(
            decision_id
        )


        if entry is None:

            return None


        data = entry.value


        return AutonomyDecision(

            decision_id=data["decision_id"],

            context_id=data["context_id"],

            strategy_id=data["strategy_id"],

            reason=data["reason"],

            confidence=data["confidence"]

        )



    def count_memories(
        self
    ) -> int:
        """
        Return number of stored autonomy memories.
        """


        return self.memory.count()