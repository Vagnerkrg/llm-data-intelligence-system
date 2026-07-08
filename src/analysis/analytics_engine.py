from src.analysis.dataframe_repository import DataFrameRepository
from src.analysis.statistics_engine import StatisticsEngine


class AnalyticsEngine:
    """
    High-level analytics engine.

    Responsible for coordinating analytical
    operations over structured datasets.

    It abstracts repository access from agents,
    making the analytical layer reusable.
    """

    def __init__(
        self,
        repository=None,
        statistics_engine=None
    ):

        self.repository = (
            repository
            if repository
            else DataFrameRepository()
        )

        self.statistics = (
            statistics_engine
            if statistics_engine
            else StatisticsEngine()
        )

    def count_rows(
        self,
        dataset_name: str
    ):

        dataframe = self.repository.get(
            dataset_name
        )

        return self.statistics.count_rows(
            dataframe
        )

    def columns(
        self,
        dataset_name: str
    ):

        dataframe = self.repository.get(
            dataset_name
        )

        return self.statistics.columns(
            dataframe
        )

    def value_counts(
        self,
        dataset_name: str,
        column: str,
        limit=5
    ):

        dataframe = self.repository.get(
            dataset_name
        )

        return self.statistics.value_counts(
            dataframe,
            column,
            limit
        )

    def describe(
        self,
        dataset_name: str
    ):

        dataframe = self.repository.get(
            dataset_name
        )

        return dataframe.describe(
            include="all"
        )

    def datasets(self):

        return self.repository.list_datasets()