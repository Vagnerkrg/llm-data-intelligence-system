from src.cognitive.memory.consolidation.consolidation_pipeline import (
    ConsolidationPipeline,
)


def create_experiences():

    return [
        {
            "content": "Query execution became faster",
            "category": "performance",
            "confidence": 0.95,
        },
        {
            "content": "Database optimization improved results",
            "category": "performance",
            "confidence": 0.90,
        },
    ]


def test_consolidation_pipeline_run():

    pipeline = ConsolidationPipeline()

    result = pipeline.run(create_experiences())

    assert result is not None


def test_consolidation_pipeline_returns_list():

    pipeline = ConsolidationPipeline()

    result = pipeline.run(create_experiences())

    assert isinstance(result, list)


def test_consolidation_pipeline_count():

    pipeline = ConsolidationPipeline()

    pipeline.run(create_experiences())

    assert pipeline.count() >= 0


def test_consolidation_pipeline_empty():

    pipeline = ConsolidationPipeline()

    result = pipeline.run([])

    assert isinstance(result, list)
