from src.agents.decision.decision_alternative import DecisionAlternative


def test_should_create_decision_alternative():
    alternative = DecisionAlternative(
        name="Analytics Strategy",
        description="Use analytics capability",
        expected_outcome="Improve analysis quality",
    )

    assert alternative.name == "Analytics Strategy"
    assert alternative.description == "Use analytics capability"
    assert alternative.expected_outcome == "Improve analysis quality"


def test_should_use_default_cost():
    alternative = DecisionAlternative(
        name="Strategy A",
        description="Test strategy",
        expected_outcome="Expected result",
    )

    assert alternative.estimated_cost == 0.0


def test_should_use_default_confidence():
    alternative = DecisionAlternative(
        name="Strategy B",
        description="Another strategy",
        expected_outcome="Another result",
    )

    assert alternative.confidence == 0.0


def test_should_create_empty_metadata_by_default():
    alternative = DecisionAlternative(
        name="Strategy C",
        description="Third strategy",
        expected_outcome="Third result",
    )

    assert alternative.metadata == {}


def test_should_store_metadata_information():
    alternative = DecisionAlternative(
        name="Strategy D",
        description="Metadata example",
        expected_outcome="Metadata result",
        metadata={
            "source": "agent",
            "priority": "high",
        },
    )

    assert alternative.metadata["source"] == "agent"
    assert alternative.metadata["priority"] == "high"


def test_should_store_complete_alternative_definition():
    alternative = DecisionAlternative(
        name="Optimized Strategy",
        description="Use optimized execution flow",
        expected_outcome="Reduce execution time",
        estimated_cost=0.25,
        confidence=0.92,
        metadata={
            "category": "optimization",
        },
    )

    assert alternative.estimated_cost == 0.25
    assert alternative.confidence == 0.92
    assert alternative.metadata["category"] == "optimization"


def test_should_allow_multiple_alternatives_with_independent_values():
    first = DecisionAlternative(
        name="Strategy One",
        description="First option",
        expected_outcome="Outcome one",
    )

    second = DecisionAlternative(
        name="Strategy Two",
        description="Second option",
        expected_outcome="Outcome two",
    )

    assert first.name != second.name
    assert first.expected_outcome != second.expected_outcome