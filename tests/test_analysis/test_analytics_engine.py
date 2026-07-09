import pandas as pd

from src.analysis.analytics_engine import AnalyticsEngine
from src.agents.data_analysis_agent import DataAnalysisAgent


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
                    ],

                    "price": [
                        10,
                        20,
                        30,
                        40
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



class TestAnalyticsEngine:


    def setup_method(self):

        self.analytics = AnalyticsEngine(
            repository=FakeRepository()
        )



    def test_count_rows(self):

        result = self.analytics.count_rows(
            "products"
        )

        assert result == 4



    def test_columns(self):

        result = self.analytics.columns(
            "products"
        )

        assert "product_category_name" in result
        assert "price" in result



    def test_value_counts(self):

        result = self.analytics.value_counts(
            "products",
            "product_category_name"
        )

        assert result["books"] == 2



    def test_describe(self):

        result = self.analytics.describe(
            "products"
        )

        assert "price" in result.columns



    def test_datasets(self):

        result = self.analytics.datasets()

        assert "products" in result
        assert "customers" in result




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