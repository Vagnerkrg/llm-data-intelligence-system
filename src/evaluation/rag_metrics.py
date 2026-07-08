from typing import Dict, List



class RAGMetrics:
    """
    Collects evaluation metrics from RAG executions.

    Responsible for measuring retrieval quality
    and routing behavior.
    """



    def evaluate(
        self,
        question: str,
        route: Dict,
        results: List[Dict],
        fallback_used: bool = False
    ) -> Dict:
        """
        Creates a metrics report from a RAG execution.
        """


        scores = [

            item["score"]

            for item in results

            if "score" in item

        ]


        sources = list(

            set(

                [

                    item["metadata"].get("source")

                    for item in results

                    if "metadata" in item

                ]

            )

        )


        best_score = (

            max(scores)

            if scores

            else 0

        )


        return {

            "question": question,

            "domain": route.get(
                "domain"
            ),

            "confidence": route.get(
                "confidence"
            ),

            "documents_found": len(
                results
            ),

            "best_score": round(
                best_score,
                4
            ),

            "sources": sources,

            "fallback_used": fallback_used

        }