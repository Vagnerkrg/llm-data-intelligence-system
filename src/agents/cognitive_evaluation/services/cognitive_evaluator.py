from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.domain.evaluation_metric import (
    EvaluationMetric,
)
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)

from src.agents.cognitive_evaluation.metrics.cognitive_score import (
    CognitiveScoreCalculator,
)
from src.agents.cognitive_evaluation.metrics.execution_quality import (
    ExecutionQualityMetric,
)
from src.agents.cognitive_evaluation.metrics.memory_effectiveness import (
    MemoryEffectivenessMetric,
)
from src.agents.cognitive_evaluation.metrics.planning_quality import (
    PlanningQualityMetric,
)
from src.agents.cognitive_evaluation.metrics.reasoning_quality import (
    ReasoningQualityMetric,
)


class CognitiveEvaluator:
    """
    Orchestrates cognitive evaluation for agent executions.

    The evaluator coordinates the individual cognitive metrics
    and consolidates their results into an EvaluationResult.

    The evaluator remains independent from the AgentRuntime.
    """

    def __init__(
        self,
        reasoning_metric: ReasoningQualityMetric | None = None,
        planning_metric: PlanningQualityMetric | None = None,
        execution_metric: ExecutionQualityMetric | None = None,
        memory_metric: MemoryEffectivenessMetric | None = None,
        score_calculator: CognitiveScoreCalculator | None = None,
    ) -> None:

        self.reasoning_metric = (
            reasoning_metric
            if reasoning_metric is not None
            else ReasoningQualityMetric()
        )

        self.planning_metric = (
            planning_metric if planning_metric is not None else PlanningQualityMetric()
        )

        self.execution_metric = (
            execution_metric
            if execution_metric is not None
            else ExecutionQualityMetric()
        )

        self.memory_metric = (
            memory_metric if memory_metric is not None else MemoryEffectivenessMetric()
        )

        self.score_calculator = (
            score_calculator
            if score_calculator is not None
            else CognitiveScoreCalculator()
        )

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:
        """
        Evaluate an agent execution.

        The evaluation process consists of:

        1. Reasoning quality evaluation.
        2. Planning quality evaluation.
        3. Execution quality evaluation.
        4. Memory effectiveness evaluation.
        5. Consolidated cognitive score calculation.
        """

        metrics = self._evaluate_metrics(context)

        cognitive_score = self.score_calculator.calculate(metrics)

        result = EvaluationResult(
            overall_score=cognitive_score.score,
            status="completed",
            metadata={
                "metrics_evaluated": len(metrics),
                "evaluator": self.__class__.__name__,
            },
        )

        for metric in metrics:
            result.add_metric(metric)

        result.add_metric(cognitive_score)

        return result

    def _evaluate_metrics(
        self,
        context: EvaluationContext,
    ) -> list[EvaluationMetric]:
        """
        Evaluate all individual cognitive capabilities.
        """

        return [
            self.reasoning_metric.evaluate(context),
            self.planning_metric.evaluate(context),
            self.execution_metric.evaluate(context),
            self.memory_metric.evaluate(context),
        ]
