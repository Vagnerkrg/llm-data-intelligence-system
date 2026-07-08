import json

from pathlib import Path


class RAGDashboard:
    """
    Aggregates RAG execution metrics.

    Reads the RAG metrics log and
    generates quality statistics.
    """


    def __init__(
        self,
        metrics_file="logs/rag_metrics.jsonl"
    ):

        self.metrics_file = Path(
            metrics_file
        )


    def load(self):

        if not self.metrics_file.exists():

            return []


        records = []


        with open(
            self.metrics_file,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if line:

                    records.append(
                        json.loads(line)
                    )


        return records



    def summary(self):

        records = self.load()


        if not records:

            return {

                "total_queries": 0,

                "average_similarity": 0,

                "average_confidence": 0,

                "fallback_rate": 0,

                "average_documents": 0,

                "top_sources": {}

            }


        total = len(records)


        average_similarity = round(

            sum(

                item["best_score"]

                for item in records

            )

            / total,

            4

        )


        average_confidence = round(

            sum(

                item["confidence"]

                for item in records

            )

            / total,

            4

        )


        average_documents = round(

            sum(

                item["documents_found"]

                for item in records

            )

            / total,

            2

        )


        fallback_rate = round(

            sum(

                1

                for item in records

                if item["fallback_used"]

            )

            / total,

            4

        )


        sources = {}


        for item in records:

            for source in item["sources"]:

                sources[source] = (

                    sources.get(source, 0)

                    + 1

                )


        return {

            "total_queries": total,

            "average_similarity": average_similarity,

            "average_confidence": average_confidence,

            "fallback_rate": fallback_rate,

            "average_documents": average_documents,

            "top_sources": dict(

                sorted(

                    sources.items(),

                    key=lambda x: x[1],

                    reverse=True

                )

            )

        }