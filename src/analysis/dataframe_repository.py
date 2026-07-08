from pathlib import Path

from src.data.data_loader import OlistDataLoader
from src.data.processed_loader import ProcessedDataLoader


class DataFrameRepository:
    """
    Repository responsible for loading and providing
    access to project datasets.

    Priority:

    1. Processed datasets (parquet)
    2. Raw datasets (CSV fallback)

    DataFrames are loaded once and kept in memory,
    allowing multiple agents to reuse the same data.
    """


    def __init__(
        self,
        data_loader=None,
        processed_loader=None
    ):

        self.data_loader = (
            data_loader
            if data_loader
            else OlistDataLoader()
        )


        self.processed_loader = (
            processed_loader
            if processed_loader
            else ProcessedDataLoader()
        )


        self._datasets = None



    def _processed_exists(self):
        """
        Checks if processed data is available.
        """

        path = Path(
            "data/processed"
        )

        return (
            path.exists()
            and
            any(
                path.glob(
                    "*.parquet"
                )
            )
        )



    def load(self):
        """
        Loads datasets into memory.

        Uses processed data when available.
        Falls back to raw CSV otherwise.
        """


        if self._datasets is None:


            if self._processed_exists():

                self._datasets = (
                    self.processed_loader.load_all()
                )


            else:

                self._datasets = (
                    self.data_loader.load_all()
                )


        return self._datasets



    def get(
        self,
        dataset_name
    ):
        """
        Returns a specific dataset.

        Raises an error if dataset does not exist.
        """


        datasets = self.load()


        if dataset_name not in datasets:

            raise ValueError(
                f"Dataset not found: {dataset_name}"
            )


        return datasets[dataset_name]



    def exists(
        self,
        dataset_name
    ):
        """
        Checks if a dataset exists.
        """


        datasets = self.load()

        return dataset_name in datasets



    def list_datasets(
        self
    ):
        """
        Returns available dataset names.
        """


        return list(
            self.load().keys()
        )