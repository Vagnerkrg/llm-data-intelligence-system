import pandas as pd

from src.agents.data_analysis_agent import DataAnalysisAgent
from src.analysis.analytics_engine import AnalyticsEngine


class FakeRepository:
    """
    Fake repository used for unit tests.
    """

    def __init__(self):

        self.datasets = {

            "products": pd.DataFrame(
                {
                    "product_category_name": [
                        "books",
                        "books",
                        "games",
                        "electronics"
                    ]
                }
            ),

            "customers": pd.DataFrame(
                {
                    "customer_id": [
                        1,
                        2,
                        3
                    ]
                }
            )

        }

    def get(
        self,
        dataset_name
    ):

        return self.datasets[dataset_name]

    def list_datasets(
        self
    ):

        return list(
            self.datasets.keys()
        )


class TestDataAnalysisAgent:

    def setup_method(self):

        analytics = AnalyticsEngine(
            repository=FakeRepository()
        )

        self.agent = DataAnalysisAgent(
            analytics_engine=analytics
        )

    def test_count_products(self):

        result = self.agent.run(
            "quantos produtos existem?"
        )

        assert result["type"] == "analysis"
        assert result["operation"] == "count_rows"
        assert result["dataset"] == "products"
        assert result["result"] == 4

    def test_count_customers(self):

        result = self.agent.run(
            "quantos clientes existem?"
        )

        assert result["dataset"] == "customers"
        assert result["result"] == 3

    def test_columns(self):

        result = self.agent.run(
            "quais são as colunas?"
        )

        assert result["operation"] == "columns"

    def test_value_counts(self):

        result = self.agent.run(
            "qual categoria possui mais produtos?"
        )

        assert result["operation"] == "value_counts"
        assert result["result"]["books"] == 2

    def test_unknown_question(self):

        result = self.agent.run(
            "abc xyz"
        )

        assert result["operation"] == "unknown"