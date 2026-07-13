from src.agents.decision.alternative_generator import AlternativeGenerator
from src.agents.decision.alternative_evaluator import AlternativeEvaluator
from src.agents.decision.decision_selector import DecisionSelector
from src.agents.decision.confidence_analyzer import ConfidenceAnalyzer
from src.agents.decision.decision_explainer import DecisionExplainer
from src.agents.decision.decision_pipeline_result import DecisionPipelineResult
from src.agents.decision.decision_context import DecisionContext


class DecisionPipeline:
    """
    Orchestrates the complete Decision Intelligence Pipeline.

    Flow:

    Context
        ↓
    Alternative Generation
        ↓
    Alternative Evaluation
        ↓
    Decision Selection
        ↓
    Confidence Analysis
        ↓
    Explanation
    """

    def __init__(self):

        self.generator = AlternativeGenerator()
        self.evaluator = AlternativeEvaluator()
        self.selector = DecisionSelector()
        self.confidence_analyzer = ConfidenceAnalyzer()
        self.explainer = DecisionExplainer()


    def run(
        self,
        context: DecisionContext
    ) -> DecisionPipelineResult:
        """
        Execute complete decision pipeline.
        """

        alternatives = self.generator.generate(
            context
        )

        evaluations = self.evaluator.evaluate(
            alternatives,
            context
        )

        decision = self.selector.select(
            alternatives,
            evaluations
        )

        confidence = self.confidence_analyzer.calculate(
            evaluations
        )

        explanation = self.explainer.explain(
            decision,
            confidence
        )

        return DecisionPipelineResult(
            decision_id=decision.decision_id,
            confidence=confidence,
            explanation=explanation
        )