from src.data.data_loader import OlistDataLoader


class DataFrameRepository:
    """
    Repository responsible for loading and providing
    access to the Olist datasets.

    DataFrames are loaded once and kept in memory,
    allowing multiple agents to reuse the same data.
    """

    def __init__(
        self,
        data_loader=None
    ):

        self.data_loader = (
            data_loader
            if data_loader
            else OlistDataLoader()
        )

        self._datasets = None


    def load(self):
        """
        Loads all datasets into memory.
        """

        if self._datasets is None:

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
        """

        datasets = self.load()

        return datasets.get(
            dataset_name
        )


    def list_datasets(
        self
    ):
        """
        Returns the available dataset names.
        """

        return list(
            self.load().keys()
        )