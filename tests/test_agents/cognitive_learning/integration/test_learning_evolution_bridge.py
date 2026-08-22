from src.agents.autonomous_evolution.domain.evolution_context import (
    EvolutionContext,
)
from src.agents.autonomous_evolution.domain.optimization_signal import (
    OptimizationSignal,
)
from src.agents.autonomous_evolution.services.evolution_decision_engine import (
    EvolutionDecisionEngine,
)
from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.cognitive_learning.integration.learning_evolution_bridge import (
    LearningEvolutionBridge,
)
from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)


def _outcome(
    *,
    experience_id: str = "exp-1",
    confidence: float = 0.9,
) -> LearningOutcome:
    return LearningOutcome(
        experience_id=experience_id,
        learned_pattern="effective strategy",
        knowledge_candidate="strategy: effective strategy",
        confidence=confidence,
        recommendation="Reuse this strategy.",
        metadata={
            "learning_type": "effective_behavior",
        },
    )


def _learning_signal(
    *,
    confidence: float = 0.8,
) -> LearningSignal:
    return LearningSignal(
        signal_type="strategy",
        pattern="effective strategy",
        confidence=confidence,
        impact="high",
        recommendation="Reuse the strategy.",
    )


def _optimization_signal(
    *,
    strength: float = 0.9,
    confidence: float = 0.8,
) -> OptimizationSignal:
    return OptimizationSignal(
        signal_type="strategy_preference",
        target="execution_strategy",
        direction="reinforce",
        strength=strength,
        confidence=confidence,
        reason=("Repeated execution outcomes indicate effectiveness."),
        supporting_patterns=[
            "effective_execution_pattern",
        ],
    )


def test_builds_evolution_context_from_learning_outcomes():
    bridge = LearningEvolutionBridge()

    context = bridge.build_context(
        learning_outcomes=[
            _outcome(),
        ]
    )

    assert isinstance(
        context,
        EvolutionContext,
    )
    assert len(context.learning_information) == 1
    assert context.learning_information[0]["source"] == "learning_outcome"
    assert context.learning_information[0]["experience_id"] == "exp-1"


def test_exposes_learning_signals_to_evolution():
    bridge = LearningEvolutionBridge()

    context = bridge.build_context(
        learning_signals=[
            _learning_signal(),
        ]
    )

    assert len(context.learning_information) == 1
    assert context.learning_information[0]["source"] == "learning_signal"
    assert context.learning_information[0]["signal_type"] == "strategy"


def test_exposes_optimization_signals_to_evolution():
    bridge = LearningEvolutionBridge()

    context = bridge.build_context(
        optimization_signals=[
            _optimization_signal(),
        ]
    )

    assert len(context.improvement_information) == 1
    assert context.improvement_information[0]["source"] == "optimization_signal"
    assert context.improvement_information[0]["direction"] == "reinforce"


def test_learning_can_contribute_to_evolution_decision():
    engine = EvolutionDecisionEngine(
        min_evidence=2,
        min_confidence=0.6,
        evolution_threshold=0.7,
    )

    bridge = LearningEvolutionBridge(
        evolution_decision_engine=engine,
    )

    result = bridge.evaluate(
        learning_outcomes=[
            _outcome(confidence=0.9),
        ],
        learning_signals=[
            _learning_signal(confidence=0.9),
        ],
    )

    assert result.should_evolve
    assert result.learning_evidence_count == 2
    assert result.decision.confidence == 0.9


def test_learning_and_optimization_can_drive_evolution():
    engine = EvolutionDecisionEngine(
        min_evidence=2,
        min_confidence=0.6,
        evolution_threshold=0.7,
    )

    bridge = LearningEvolutionBridge(
        evolution_decision_engine=engine,
    )

    result = bridge.evaluate(
        learning_outcomes=[
            _outcome(confidence=0.8),
        ],
        optimization_signals=[
            _optimization_signal(
                strength=0.9,
                confidence=0.8,
            ),
        ],
    )

    assert result.should_evolve
    assert result.learning_evidence_count == 1
    assert result.optimization_signal_count == 1
    assert len(result.decision.evidence) == 2


def test_preserves_base_evolution_context():
    bridge = LearningEvolutionBridge()

    base_context = EvolutionContext(
        execution_information={
            "score": 0.8,
            "confidence": 0.9,
        },
        evaluation_information={
            "score": 0.9,
            "confidence": 0.9,
        },
        knowledge_information={
            "score": 0.8,
            "confidence": 0.8,
        },
        metadata={
            "question": "test",
        },
    )

    context = bridge.build_context(
        learning_outcomes=[
            _outcome(),
        ],
        base_context=base_context,
    )

    assert context.execution_information == (base_context.execution_information)
    assert context.evaluation_information == (base_context.evaluation_information)
    assert context.knowledge_information == (base_context.knowledge_information)
    assert context.metadata == {
        "question": "test",
    }
    assert len(context.learning_information) == 1


def test_dependency_injection_preserves_engine_identity():
    engine = EvolutionDecisionEngine()

    bridge = LearningEvolutionBridge(
        evolution_decision_engine=engine,
    )

    assert bridge.evolution_decision_engine is engine


def test_rejects_invalid_base_context():
    bridge = LearningEvolutionBridge()

    try:
        bridge.build_context(
            base_context="invalid",
        )
    except TypeError as error:
        assert "base_context" in str(error)
    else:
        raise AssertionError("Expected TypeError was not raised.")


def test_rejects_invalid_learning_outcome():
    bridge = LearningEvolutionBridge()

    try:
        bridge.build_context(
            learning_outcomes=[
                "invalid",
            ]
        )
    except TypeError as error:
        assert "learning_outcomes" in str(error)
    else:
        raise AssertionError("Expected TypeError was not raised.")


def test_rejects_invalid_learning_signal():
    bridge = LearningEvolutionBridge()

    try:
        bridge.build_context(
            learning_signals=[
                "invalid",
            ]
        )
    except TypeError as error:
        assert "learning_signals" in str(error)
    else:
        raise AssertionError("Expected TypeError was not raised.")


def test_rejects_invalid_optimization_signal():
    bridge = LearningEvolutionBridge()

    try:
        bridge.build_context(
            optimization_signals=[
                "invalid",
            ]
        )
    except TypeError as error:
        assert "optimization_signals" in str(error)
    else:
        raise AssertionError("Expected TypeError was not raised.")


def test_evaluation_is_deterministic():
    engine = EvolutionDecisionEngine(
        min_evidence=2,
        min_confidence=0.6,
        evolution_threshold=0.7,
    )

    bridge = LearningEvolutionBridge(
        evolution_decision_engine=engine,
    )

    first = bridge.evaluate(
        learning_outcomes=[
            _outcome(
                experience_id="exp-1",
                confidence=0.9,
            ),
        ],
        learning_signals=[
            _learning_signal(
                confidence=0.8,
            ),
        ],
    )

    second = bridge.evaluate(
        learning_outcomes=[
            _outcome(
                experience_id="exp-1",
                confidence=0.9,
            ),
        ],
        learning_signals=[
            _learning_signal(
                confidence=0.8,
            ),
        ],
    )

    assert first.context.to_dict() == second.context.to_dict()
    assert first.decision.should_evolve == second.decision.should_evolve
    assert first.decision.confidence == second.decision.confidence
