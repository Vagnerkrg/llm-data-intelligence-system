from typing import Any

from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.runtime.execution_context import ExecutionContext


class CognitiveEvaluationAdapter:
    """
    Adapts runtime execution state into cognitive evaluation context.

    The adapter is responsible only for translating information
    between the runtime layer and the cognitive evaluation layer.

    It does not calculate metrics or perform evaluation logic.
    """

    def adapt(
        self,
        execution_context: ExecutionContext,
    ) -> EvaluationContext:
        """
        Convert an ExecutionContext into an EvaluationContext.
        """

        if not isinstance(
            execution_context,
            ExecutionContext,
        ):
            raise TypeError("execution_context must be an ExecutionContext instance.")

        return EvaluationContext(
            execution_result=self._build_execution_result(execution_context),
            reasoning_information=self._build_reasoning_information(execution_context),
            planning_information=self._build_planning_information(execution_context),
            memory_information=self._build_memory_information(execution_context),
            improvement_information=(execution_context.cognitive_improvement),
            metadata={
                "question": execution_context.question,
                "status": execution_context.status,
            },
        )

    @staticmethod
    def _build_execution_result(
        context: ExecutionContext,
    ) -> dict[str, Any]:
        """
        Build execution information required by evaluation metrics.
        """

        completed_steps = float(
            sum(1 for result in context.results if result is not None)
        )

        failed_steps = 0.0

        if context.plan is not None:
            failed_steps = float(
                sum(1 for step in context.plan.steps if step.status == "failed")
            )

        execution_efficiency = 1.0 if context.status == "completed" else 0.0

        return {
            "execution_status": context.status,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "execution_efficiency": execution_efficiency,
        }

    @staticmethod
    def _build_reasoning_information(
        context: ExecutionContext,
    ) -> dict[str, Any] | None:
        """
        Extract normalized reasoning information.
        """

        reasoning = context.reasoning

        if reasoning is None:
            return None

        if isinstance(reasoning, dict):
            return reasoning

        result: dict[str, Any] = {}

        confidence = getattr(
            reasoning,
            "confidence",
            None,
        )

        strategy = getattr(
            reasoning,
            "strategy",
            None,
        )

        conclusion = getattr(
            reasoning,
            "conclusion",
            None,
        )

        if confidence is not None:
            result["confidence"] = confidence

        if strategy:
            result["strategy"] = 1.0

        if conclusion:
            result["conclusion_quality"] = 1.0

        reasoning_text = getattr(
            reasoning,
            "reasoning",
            None,
        )

        if reasoning_text:
            result["completeness"] = 1.0

        return result or None

    @staticmethod
    def _build_planning_information(
        context: ExecutionContext,
    ) -> dict[str, Any] | None:
        """
        Extract normalized planning information.
        """

        plan = context.plan

        if plan is None:
            return None

        total_steps = len(plan.steps)

        if total_steps == 0:
            return {
                "execution_steps": 0.0,
                "step_consistency": 0.0,
                "dependency_resolution": 0.0,
                "plan_completeness": 0.0,
            }

        completed_steps = sum(1 for step in plan.steps if step.status == "completed")

        failed_steps = sum(1 for step in plan.steps if step.status == "failed")

        execution_steps = min(
            1.0,
            total_steps / max(total_steps, 1),
        )

        step_consistency = (
            1.0
            if failed_steps == 0
            else max(
                0.0,
                1.0 - (failed_steps / total_steps),
            )
        )

        dependency_resolution = 1.0 if failed_steps == 0 else 0.0

        plan_completeness = completed_steps / total_steps

        return {
            "execution_steps": execution_steps,
            "step_consistency": step_consistency,
            "dependency_resolution": dependency_resolution,
            "plan_completeness": plan_completeness,
        }

    @staticmethod
    def _build_memory_information(
        context: ExecutionContext,
    ) -> dict[str, Any] | None:
        """
        Extract normalized memory information.
        """

        memory_context = context.memory_context

        if memory_context is None:
            return None

        if isinstance(memory_context, dict):
            return memory_context

        return {
            "memory_usage": 1.0,
            "relevance_score": 1.0,
            "retrieved_context_quality": 1.0,
            "memory_contribution": 1.0,
        }
