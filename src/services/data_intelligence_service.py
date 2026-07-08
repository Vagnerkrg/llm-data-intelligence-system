from src.analysis.analytics_engine import AnalyticsEngine
from src.logging import AppLogger


class DataIntelligenceService:
    """
    Service layer responsible for data intelligence operations.

    Provides a stable interface between agents
    and analytical components.
    """


    def __init__(
        self,
        analytics_engine=None
    ):

        self.analytics = (
            analytics_engine
            if analytics_engine
            else AnalyticsEngine()
        )


        self.logger = AppLogger(
            self.__class__.__name__
        )



    def count_dataset_rows(
        self,
        dataset_name
    ):
        """
        Counts rows from a dataset.
        """

        self.logger.info(
            f"[DATA_SERVICE] Counting rows: {dataset_name}"
        )


        return self.analytics.count_rows(
            dataset_name
        )



    def get_dataset_columns(
        self,
        dataset_name
    ):
        """
        Returns dataset columns.
        """

        self.logger.info(
            f"[DATA_SERVICE] Getting columns: {dataset_name}"
        )


        return self.analytics.columns(
            dataset_name
        )



    def get_value_counts(
        self,
        dataset_name,
        column,
        limit=5
    ):
        """
        Returns frequency distribution.
        """

        self.logger.info(
            f"[DATA_SERVICE] Value counts: {dataset_name}.{column}"
        )


        return self.analytics.value_counts(
            dataset_name,
            column,
            limit
        )