from pathlib import Path

import pandas as pd

from src.data.document_builder import DocumentBuilder
from src.embeddings.local_embedding import LocalEmbeddingGenerator
from src.index.vector_index import VectorIndex



class BuildIndex:
    """
    Builds a vector index from processed datasets.
    """


    def __init__(
        self,
        data_path="data/processed"
    ):

        self.data_path = Path(data_path)

        self.document_builder = DocumentBuilder()

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



    def build(self, limit=1000):
        """
        Creates documents, embeddings and vector index.
        """

        datasets = self.load_processed_data()


        documents = self.document_builder.build_from_datasets(
            datasets,
            limit=limit
        )


        embeddings = self.embedding_generator.generate(
            documents
        )


        self.vector_index.add(
            embeddings,
            documents
        )


        self.vector_index.save()


        return {
            "datasets": list(datasets.keys()),
            "documents": len(documents),
            "vectors": len(embeddings)
        }



if __name__ == "__main__":

    builder = BuildIndex()

    result = builder.build()

    print("Vector index created")

    print(result)