import numpy as np
from pathlib import Path
import pickle


class VectorIndex:
    """
    Local vector index.

    Responsible for storing embeddings
    and performing similarity search.
    """


    def __init__(
        self,
        index_path="models/vector_index.pkl"
    ):

        self.index_path = Path(index_path)

        self.vectors = []
        self.documents = []


    def add(
        self,
        embeddings,
        documents
    ):
        """
        Adds embeddings and associated documents.
        """

        self.vectors.extend(
            embeddings
        )

        self.documents.extend(
            documents
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
            "documents": self.documents
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

            data = pickle.load(file)


        self.vectors = data["vectors"]
        self.documents = data["documents"]


    def search(
        self,
        query_embedding,
        top_k=3
    ):
        """
        Performs cosine similarity search.
        """

        vectors = np.array(
            self.vectors
        )


        query = np.array(
            query_embedding
        )


        similarities = (
            vectors @ query
            /
            (
                np.linalg.norm(vectors, axis=1)
                *
                np.linalg.norm(query)
            )
        )


        indexes = np.argsort(
            similarities
        )[::-1][:top_k]


        results = []

        for index in indexes:

            results.append(
                {
                    "document": self.documents[index],
                    "score": float(
                        similarities[index]
                    )
                }
            )


        return results