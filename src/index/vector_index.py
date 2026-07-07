import numpy as np
from pathlib import Path
import pickle



class VectorIndex:
    """
    Local vector index with metadata support.

    Responsible for storing embeddings,
    documents and metadata for filtered retrieval.
    """



    def __init__(
        self,
        index_path="models/vector_index.pkl"
    ):

        self.index_path = Path(index_path)

        self.vectors = []

        self.documents = []

        self.metadata = []



    def add(
        self,
        embeddings,
        documents,
        metadata=None
    ):
        """
        Adds embeddings, documents and metadata.
        """


        self.vectors.extend(
            embeddings
        )


        self.documents.extend(
            documents
        )


        if metadata:

            self.metadata.extend(
                metadata
            )

        else:

            self.metadata.extend(
                [
                    {}
                    for _ in documents
                ]
            )



    def save(self):
        """
        Saves vector index locally.
        """


        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        data = {

            "vectors": self.vectors,

            "documents": self.documents,

            "metadata": self.metadata

        }


        with open(
            self.index_path,
            "wb"
        ) as file:

            pickle.dump(
                data,
                file
            )



    def load(self):
        """
        Loads existing vector index.
        """


        if not self.index_path.exists():

            raise FileNotFoundError(
                "Vector index not found."
            )



        with open(
            self.index_path,
            "rb"
        ) as file:

            data = pickle.load(
                file
            )



        self.vectors = data["vectors"]

        self.documents = data["documents"]


        self.metadata = data.get(
            "metadata",
            [
                {}
                for _ in self.documents
            ]
        )



    def search(
        self,
        query_embedding,
        top_k=3,
        source=None
    ):
        """
        Performs cosine similarity search.

        Optional filtering by metadata source.
        """


        vectors = np.array(
            self.vectors
        )


        query = np.array(
            query_embedding
        )



        indexes_pool = range(
            len(self.documents)
        )



        if source:


            indexes_pool = [

                index

                for index in indexes_pool

                if self.metadata[index].get(
                    "source"
                ) == source

            ]



        if not indexes_pool:

            return []



        filtered_vectors = vectors[
            list(indexes_pool)
        ]



        similarities = (

            filtered_vectors @ query

            /

            (
                np.linalg.norm(
                    filtered_vectors,
                    axis=1
                )

                *

                np.linalg.norm(
                    query
                )
            )

        )



        sorted_positions = np.argsort(
            similarities
        )[::-1][:top_k]



        results = []



        for position in sorted_positions:

            original_index = list(
                indexes_pool
            )[position]


            results.append(

                {

                    "document": self.documents[original_index],

                    "metadata": self.metadata[original_index],

                    "score": float(
                        similarities[position]
                    )

                }

            )



        return results