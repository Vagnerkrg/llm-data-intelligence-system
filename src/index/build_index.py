from pathlib import Path

import pandas as pd

from src.data.document_builder import DocumentBuilder
from src.data.summary_builder import SummaryBuilder
from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex



class BuildIndex:
    """
    Builds a vector index from processed datasets
    using semantic documents, summaries and metadata.
    """



    def __init__(
        self,
        data_path="data/processed"
    ):

        self.data_path = Path(data_path)

        self.document_builder = DocumentBuilder()

        self.summary_builder = SummaryBuilder()

        self.embedding_generator = LocalEmbeddingGenerator()

        self.vector_index = VectorIndex()



    def load_processed_data(self):
        """
        Loads processed parquet datasets.
        """

        datasets = {}


        for file in self.data_path.glob("*.parquet"):

            datasets[file.stem] = pd.read_parquet(
                file
            )


        return datasets



    def build(
        self,
        limit=1000
    ):
        """
        Creates documents, summaries, embeddings and vector index.
        """


        datasets = self.load_processed_data()



        documents = self.document_builder.build_from_datasets(
            datasets,
            limit=limit
        )


        summaries = self.summary_builder.build_dataset_summaries(
            datasets
        )


        documents.extend(
            [
                {
                    "text": summary,
                    "metadata": {
                        "source": "summary",
                        "type": "analytical"
                    }
                }

                for summary in summaries
            ]
        )



        texts = [
            document["text"]
            for document in documents
        ]


        metadata = [
            document["metadata"]
            for document in documents
        ]



        embeddings = self.embedding_generator.generate(
            texts
        )



        self.vector_index.add(
            embeddings,
            texts,
            metadata
        )



        self.vector_index.save()



        return {
            "datasets": list(datasets.keys()),
            "documents": len(texts),
            "vectors": len(embeddings),
            "summaries": len(summaries)
        }




if __name__ == "__main__":


    builder = BuildIndex()


    result = builder.build()


    print("Vector index created")

    print(result)