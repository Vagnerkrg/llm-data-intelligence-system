import json

from src.evaluation.rag_dashboard import RAGDashboard


def test_rag_dashboard_summary(tmp_path):

    metrics = [

        {

            "best_score": 0.80,

            "confidence": 0.90,

            "documents_found": 3,

            "fallback_used": False,

            "sources": [

                "products",

                "orders"

            ]

        },

        {

            "best_score": 0.60,

            "confidence": 0.70,

            "documents_found": 2,

            "fallback_used": True,

            "sources": [

                "products"

            ]

        }

    ]


    file = tmp_path / "rag_metrics.jsonl"


    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        for item in metrics:

            f.write(
                json.dumps(item)
                + "\n"
            )


    dashboard = RAGDashboard(
        file
    )


    summary = dashboard.summary()


    assert summary["total_queries"] == 2

    assert summary["average_similarity"] == 0.7

    assert summary["average_confidence"] == 0.8

    assert summary["average_documents"] == 2.5

    assert summary["fallback_rate"] == 0.5

    assert summary["top_sources"]["products"] == 2

    assert summary["top_sources"]["orders"] == 1