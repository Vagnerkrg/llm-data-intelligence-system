from typing import Dict

from src.analysis.dataframe_repository import DataFrameRepository
from src.analysis.statistics_engine import StatisticsEngine



class DataAnalysisAgent:
    """
    Agent responsible for structured data analysis.

    Uses pandas datasets through the repository
    and executes analytical operations.
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


        self.statistics_engine = (
            statistics_engine
            if statistics_engine
            else StatisticsEngine()
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Executes analytical questions.
        """


        text = question.lower()



        # Count products

        if "quantos produtos" in text:

            products = self.repository.get(
                "products"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "products",

                "result": self.statistics_engine.count_rows(
                    products
                )

            }



        # Count customers

        if "quantos clientes" in text:

            customers = self.repository.get(
                "customers"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "customers",

                "result": self.statistics_engine.count_rows(
                    customers
                )

            }



        # Product columns

        if "colunas" in text:

            products = self.repository.get(
                "products"
            )


            return {

                "type": "analysis",

                "operation": "columns",

                "dataset": "products",

                "result": self.statistics_engine.columns(
                    products
                )

            }



        # Most frequent product categories

        if (
            "categoria" in text
            and
            (
                "mais" in text
                or
                "maior" in text
                or
                "possui" in text
            )
        ):

            products = self.repository.get(
                "products"
            )


            return {

                "type": "analysis",

                "operation": "value_counts",

                "dataset": "products",

                "column": "product_category_name",

                "result": self.statistics_engine.value_counts(
                    products,
                    "product_category_name",
                    limit=5
                )

            }



        return {

            "type": "analysis",

            "operation": "unknown",

            "result": "Pergunta analítica não reconhecida."

        }