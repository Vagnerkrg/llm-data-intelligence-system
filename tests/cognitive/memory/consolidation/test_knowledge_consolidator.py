from src.cognitive.memory.consolidation.knowledge_consolidator import (
    KnowledgeConsolidator
)



def create_candidates():

    return [

        {
            "content":
                "Optimize database queries",

            "source_pattern":
                "query-pattern",

            "confidence":
                0.95
        },

        {
            "content":
                "Weak information",

            "source_pattern":
                "weak-pattern",

            "confidence":
                0.2
        }

    ]



def test_knowledge_consolidator_create():

    consolidator = KnowledgeConsolidator()


    result = consolidator.consolidate(
        create_candidates()
    )


    assert len(result) == 1



def test_knowledge_consolidator_filter():

    consolidator = KnowledgeConsolidator(
        confidence_threshold=0.9
    )


    result = consolidator.consolidate(
        create_candidates()
    )


    assert len(result) == 1



def test_knowledge_consolidator_count():

    consolidator = KnowledgeConsolidator()


    consolidator.consolidate(
        create_candidates()
    )


    assert consolidator.count() == 1



def test_knowledge_consolidator_get_all():

    consolidator = KnowledgeConsolidator()


    consolidator.consolidate(
        create_candidates()
    )


    result = consolidator.get_all()


    assert len(result) == 1