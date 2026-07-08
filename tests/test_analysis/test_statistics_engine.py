import pandas as pd

from src.analysis.statistics_engine import StatisticsEngine


class TestStatisticsEngine:


    def setup_method(self):

        self.engine = StatisticsEngine()



    def test_count_rows(self):
        """
        Validates row counting.
        """

        dataframe = pd.DataFrame(
            [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ]
        )

        result = self.engine.count_rows(
            dataframe
        )

        assert result == 2



    def test_columns(self):
        """
        Validates column extraction.
        """

        dataframe = pd.DataFrame(
            [
                {
                    "id": 1,
                    "category": "phone"
                }
            ]
        )

        result = self.engine.columns(
            dataframe
        )

        assert "id" in result
        assert "category" in result



    def test_value_counts(self):
        """
        Validates frequency analysis.
        """

        dataframe = pd.DataFrame(
            [
                {
                    "category": "phone"
                },
                {
                    "category": "book"
                },
                {
                    "category": "phone"
                }
            ]
        )

        result = self.engine.value_counts(
            dataframe,
            "category"
        )

        assert result["phone"] == 2
        assert result["book"] == 1



    def test_missing_column(self):
        """
        Validates invalid column handling.
        """

        dataframe = pd.DataFrame(
            [
                {
                    "category": "phone"
                }
            ]
        )

        result = self.engine.value_counts(
            dataframe,
            "invalid"
        )

        assert "error" in result