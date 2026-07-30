from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationResult,
)

from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)

from src.cognitive.evaluation.intelligence.evaluation_interpreter import (
    EvaluationInterpreter,
)

from src.cognitive.evaluation.intelligence.evaluation_interpretation import (
    EvaluationInterpretation,
)


def test_interpreter_creates_interpretation():

    result = EvaluationResult(
        evaluation_id="eval-001",
        score=0.9,
        quality_level="high",
        signals=[],
    )

    interpreter = EvaluationInterpreter()

    interpretation = interpreter.interpret(
        result
    )

    assert isinstance(
        interpretation,
        EvaluationInterpretation
    )

    assert interpretation.severity == "low"


def test_interpreter_detects_high_risk_signal():

    signal = LearningSignal(
        signal_type="reasoning",
        pattern="incorrect_decision",
        confidence=0.9,
        impact="high",
        recommendation="improve reasoning",
    )


    result = EvaluationResult(
        evaluation_id="eval-002",
        score=0.4,
        quality_level="medium",
        signals=[
            signal
        ],
    )


    interpreter = EvaluationInterpreter()


    interpretation = interpreter.interpret(
        result
    )


    assert interpretation.requires_improvement is True

    assert "reasoning" in interpretation.areas