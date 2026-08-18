from typing import Any, Dict, Optional

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.goal import Goal
from src.agents.reasoning.reasoning_result import ReasoningResult


class ExecutionContext:
    """
    Stores runtime information during an agent execution.

    The context keeps the current state shared between reasoning,
    planning, execution, cognitive evaluation, improvement, memory,
    learning, and autonomous evolution layers.
    """

    def __init__(
        self,
        question: str,
        plan: Optional[ExecutionPlan] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.question = question
        self.plan = plan

        self.reasoning_result = None
        self.reasoning = None
        self.goal = None

        self.cognitive_improvement = None
        self.memory_context = None
        self.cognitive_evaluation = None

        self.learning_experiences = []
        self.learning_outcomes = []
        self.learning_loop_result = None

        self.evolution_decision = None
        self.evolution_result = None
        self.adaptation_action = None

        self.current_step = None
        self.results = []

        self.metadata = (
            metadata
            if metadata is not None
            else {}
        )

        self.status = "initialized"

    def set_reasoning(
        self,
        reasoning_result: ReasoningResult,
    ):
        self.reasoning_result = reasoning_result
        self.reasoning = reasoning_result

    def set_goal(
        self,
        goal: Goal,
    ):
        self.goal = goal

    def set_cognitive_evaluation(
        self,
        evaluation_result: Any,
    ):
        self.cognitive_evaluation = evaluation_result

    def set_cognitive_improvement(
        self,
        improvement_result: Any,
    ):
        self.cognitive_improvement = improvement_result

    def set_memory_context(
        self,
        memory_context: Any,
    ):
        self.memory_context = memory_context

    def set_learning_experiences(
        self,
        learning_experiences: Any,
    ):
        self.learning_experiences = list(
            learning_experiences
        )

    def set_learning_outcomes(
        self,
        learning_outcomes: Any,
    ):
        self.learning_outcomes = list(
            learning_outcomes
        )

    def set_learning_loop_result(
        self,
        learning_loop_result: Any,
    ):
        self.learning_loop_result = learning_loop_result

        if learning_loop_result is None:
            return

        experiences = getattr(
            learning_loop_result,
            "learning_experiences",
            None,
        )

        outcomes = getattr(
            learning_loop_result,
            "learning_outcomes",
            None,
        )

        if experiences is not None:
            self.set_learning_experiences(
                experiences
            )

        if outcomes is not None:
            self.set_learning_outcomes(
                outcomes
            )

    def set_evolution_decision(
        self,
        evolution_decision: Any,
    ):
        self.evolution_decision = evolution_decision

    def set_evolution_result(
        self,
        evolution_result: Any,
    ):
        self.evolution_result = evolution_result

    def set_adaptation_action(
        self,
        adaptation_action: Any,
    ):
        self.adaptation_action = adaptation_action

    def set_plan(
        self,
        plan: ExecutionPlan,
    ):
        self.plan = plan
        self.status = "planned"

    def update_current_step(
        self,
    ):
        if not self.plan:
            self.current_step = None
            return

        self.current_step = self.plan.next_step()

    def clear_current_step(
        self,
    ):
        self.current_step = None

    def add_result(
        self,
        result: Any,
    ):
        self.results.append(result)

    def complete(
        self,
    ):
        self.status = "completed"

    def fail(
        self,
        error: str,
    ):
        self.status = "failed"
        self.metadata["error"] = error

    def summary(
        self,
    ) -> Dict[str, Any]:
        return {
            "question": self.question,
            "status": self.status,
            "has_reasoning": (
                self.reasoning is not None
            ),
            "has_goal": (
                self.goal is not None
            ),
            "goal_type": (
                getattr(
                    self.goal,
                    "goal_type",
                    None,
                )
                if self.goal
                else None
            ),
            "current_step": (
                self.current_step.action
                if self.current_step
                else None
            ),
            "results_count": len(
                self.results
            ),
            "has_plan": (
                self.plan is not None
            ),
            "has_memory_context": (
                self.memory_context is not None
            ),
            "has_cognitive_evaluation": (
                self.cognitive_evaluation is not None
            ),
            "has_learning_experiences": bool(
                self.learning_experiences
            ),
            "learning_experiences_count": len(
                self.learning_experiences
            ),
            "has_learning_outcomes": bool(
                self.learning_outcomes
            ),
            "learning_outcomes_count": len(
                self.learning_outcomes
            ),
            "has_learning_loop_result": (
                self.learning_loop_result is not None
            ),
            "has_evolution_decision": (
                self.evolution_decision is not None
            ),
            "has_evolution_result": (
                self.evolution_result is not None
            ),
            "has_adaptation_action": (
                self.adaptation_action is not None
            ),
        }