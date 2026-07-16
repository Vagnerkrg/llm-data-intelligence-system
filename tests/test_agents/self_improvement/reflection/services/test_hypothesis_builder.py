from src.agents.self_improvement.reflection.services import (
    HypothesisBuilder,
)


def test_should_initialize_hypothesis_builder():

    builder = HypothesisBuilder()

    assert builder is not None


def test_should_build_hypothesis_from_pattern():

    builder = HypothesisBuilder()

    pattern = {
        "type": "performance",
        "description": "Execution improved over time",
    }

    hypothesis = builder.build(pattern)

    assert hypothesis is not None


def test_should_generate_hypothesis_description():

    builder = HypothesisBuilder()

    pattern = {
        "type": "execution",
        "description": "Tool selection became more efficient",
    }

    hypothesis = builder.build(pattern)

    assert hypothesis.description is not None
