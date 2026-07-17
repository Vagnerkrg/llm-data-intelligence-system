from ..domain.improvement_context import ImprovementContext
from ..domain.improvement_result import ImprovementResult
from ..domain.improvement_status import ImprovementStatus

from ..integration.evaluation_adapter import EvaluationAdapter
from ..integration.reflection_adapter import ReflectionAdapter
from ..integration.learning_adapter import LearningAdapter
from ..integration.knowledge_adapter import KnowledgeAdapter
from ..integration.adaptation_adapter import AdaptationAdapter


class CycleExecutor:
    """
    Executes the cognitive improvement cycle.

    Cognitive Loop:

    Context
        |
        v
    Evaluation
        |
        v
    Reflection
        |
        v
    Learning
        |
        v
    Knowledge
        |
        v
    Adaptation
        |
        v
    ImprovementResult
    """


    def __init__(
        self,
        evaluation_adapter: EvaluationAdapter | None = None,
        reflection_adapter: ReflectionAdapter | None = None,
        learning_adapter: LearningAdapter | None = None,
        knowledge_adapter: KnowledgeAdapter | None = None,
        adaptation_adapter: AdaptationAdapter | None = None,
    ):

        self.evaluation_adapter = (
            evaluation_adapter
            if evaluation_adapter
            else EvaluationAdapter()
        )

        self.reflection_adapter = (
            reflection_adapter
            if reflection_adapter
            else ReflectionAdapter()
        )

        self.learning_adapter = (
            learning_adapter
            if learning_adapter
            else LearningAdapter()
        )

        self.knowledge_adapter = (
            knowledge_adapter
            if knowledge_adapter
            else KnowledgeAdapter()
        )

        self.adaptation_adapter = (
            adaptation_adapter
            if adaptation_adapter
            else AdaptationAdapter()
        )


    def execute(
        self,
        context: ImprovementContext
    ) -> ImprovementResult:
        """
        Execute cognitive improvement cycle.

        Flow:

        Context
            |
        Evaluation
            |
        Reflection
            |
        Learning
            |
        Knowledge
            |
        Adaptation
            |
        ImprovementResult
        """


        evaluation = self.evaluation_adapter.execute(
            context
        )


        reflection = self.reflection_adapter.execute(
            evaluation
        )


        learning = self.learning_adapter.execute(
            reflection
        )


        knowledge = self.knowledge_adapter.execute(
            learning
        )


        adaptation = self.adaptation_adapter.execute(
            knowledge
        )


        return ImprovementResult(
            status=ImprovementStatus.COMPLETED,

            insights=[
                "Cognitive improvement cycle completed."
            ],

            knowledge=[
                knowledge
            ],

            adaptations=[
                adaptation
            ],

            metadata={
                "evaluation": evaluation,
                "reflection": reflection,
                "learning": learning,
            }
        )