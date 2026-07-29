from src.cognitive.learning.protocols.learning_consolidation_protocol import (
    LearningConsolidationProtocol
)


def test_learning_consolidation_protocol_exists():

    assert LearningConsolidationProtocol is not None



def test_protocol_requires_consolidation_method():

    method = getattr(
        LearningConsolidationProtocol,
        "consolidate"
    )

    assert callable(method)