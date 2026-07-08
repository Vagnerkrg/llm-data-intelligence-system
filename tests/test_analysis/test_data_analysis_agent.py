import pandas as pd

from src.agents.data_analysis_agent import DataAnalysisAgent


class FakeRepository:
    """
    Fake repository used for testing.
    """

    def get(self, dataset):

        if dataset == "products":

            return pd.DataFrame(
                [
                    {
                        "product_category_name": "phone"
                    },
                    {
                        "product_category_name": "book"
                    },
                    {
                        "product_category_name": "phone"
                    }
                ]
            )


        if dataset == "customers":

            return pd.DataFrame(
                [
                    {
                        "customer_id": 1
                    },
                    {
                        "customer_id": 2
                    }
                ]
            )


        return pd.DataFrame()


class TestDataAnalysisAgent:


    def setup_method(self):

        self.agent = DataAnalysisAgent(
            repository=FakeRepository()
        )



    def test_count_products(self):
        """
        Validates product counting.
        """

        result = self.agent.run(
            "Quantos produtos existem?"
        )

        assert result["type"] == "analysis"
        assert result["operation"] == "count_rows"
        assert result["dataset"] == "products"
        assert result["result"] == 3



    def test_count_customers(self):
        """
        Validates customer counting.
        """

        result = self.agent.run(
            "Quantos clientes existem?"
        )

        assert result["operation"] == "count_rows"
        assert result["dataset"] == "customers"
        assert result["result"] == 2



    def test_columns(self):
        """
        Validates column retrieval.
        """

        result = self.agent.run(
            "Quais colunas existem?"
        )

        assert result["operation"] == "columns"
        assert "product_category_name" in result["result"]



    def test_value_counts(self):
        """
        Validates category frequency analysis.
        """

        result = self.agent.run(
            "Qual categoria possui mais produtos?"
        )

        assert result["operation"] == "value_counts"
        assert result["result"]["phone"] == 2
        assert result["result"]["book"] == 1



    def test_unknown_question(self):
        """
        Validates unsupported analytical questions.
        """

        result = self.agent.run(
            "Qual é a cor do céu?"
        )

        assert result["operation"] == "unknown"