from dataclasses import dataclass, field

from .observation import Observation
from .reflection import ReflectionResult
from .learning import LearningSignal
from .adaptation import AdaptationStrategy
from .decision import AutonomyDecision

from src.agents.memory.autonomy_memory import AutonomyMemory



@dataclass(slots=True)
class AutonomyEngine:
    """
    Responsible for evaluating agent behavior
    after execution.

    The engine observes outcomes,
    generates reflections,
    extracts learning signals,
    stores experiences,
    and produces controlled adaptation decisions.
    """


    memory: AutonomyMemory = field(
        default_factory=AutonomyMemory
    )



    def evaluate_execution(
        self,
        execution_id: str,
        result: str,
        success: bool,
        metrics: dict[str, float] | None = None,
    ) -> AutonomyDecision:
        """
        Evaluates an execution outcome.
        """


        observation = Observation(

            observation_id=f"obs-{execution_id}",

            context_id=execution_id,

            execution_id=execution_id,

            observation_type=(
                "SUCCESS"
                if success
                else "FAILURE"
            ),

            state=result,

            metrics=metrics or {},

        )


        reflection = self._reflect(
            observation
        )


        learning = self._learn(
            reflection
        )


        #
        # V1.16 Memory Integration
        #
        # Store learned experience
        # for future decisions.
        #

        self.memory.store_learning(
            learning
        )


        strategy = self._adapt(
            learning
        )


        return AutonomyDecision(

            decision_id=f"auto-{execution_id}",

            context_id=execution_id,

            strategy_id=strategy.strategy_id,

            reason=reflection.analysis,

            confidence=reflection.confidence,

        )




    def _reflect(
        self,
        observation: Observation,
    ) -> ReflectionResult:
        """
        Generates reflection from observation.
        """


        if observation.observation_type == "SUCCESS":

            analysis = (
                "Execution succeeded. "
                "Current strategy produced positive outcome."
            )

            confidence = 0.8


        else:

            analysis = (
                "Execution failed. "
                "Strategy should be reviewed."
            )

            confidence = 0.7



        return ReflectionResult(

            reflection_id=(
                f"reflection-{observation.observation_id}"
            ),

            observation_id=observation.observation_id,

            analysis=analysis,

            findings=[
                observation.observation_type
            ],

            confidence=confidence,

            recommendations=[
                "Evaluate future execution strategy"
            ],

        )




    def _learn(
        self,
        reflection: ReflectionResult,
    ) -> LearningSignal:
        """
        Extracts learning information.
        """


        return LearningSignal(

            signal_id=(
                f"learning-{reflection.reflection_id}"
            ),

            reflection_id=reflection.reflection_id,

            source="autonomy_engine",

            pattern=reflection.analysis,

            impact="behavior_improvement",

            confidence=reflection.confidence,

        )




    def _adapt(
        self,
        learning: LearningSignal,
    ) -> AdaptationStrategy:
        """
        Creates an adaptation proposal.
        """


        return AdaptationStrategy(

            strategy_id=(
                f"strategy-{learning.signal_id}"
            ),

            learning_signal_id=learning.signal_id,

            trigger=learning.pattern,

            action="review_execution_strategy",

            expected_effect=learning.impact,

            confidence=learning.confidence,

        )