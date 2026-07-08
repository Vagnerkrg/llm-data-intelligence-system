from typing import Dict

from src.analysis.dataframe_repository import DataFrameRepository
from src.analysis.statistics_engine import StatisticsEngine
from src.logging import AppLogger



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


        self.logger = AppLogger(
            self.__class__.__name__
        )



    def run(
        self,
        question: str
    ) -> Dict:
        """
        Executes analytical questions.
        """


        self.logger.info(
            f"[ANALYSIS_AGENT] Question received: {question}"
        )


        text = question.lower()



        # Count products

        if "quantos produtos" in text:


            self.logger.info(
                "[ANALYSIS_AGENT] Operation: count products"
            )


            products = self.repository.get(
                "products"
            )


            result = self.statistics_engine.count_rows(
                products
            )


            self.logger.info(
                f"[ANALYSIS_AGENT] Products count result: {result}"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "products",

                "result": result

            }



        # Count customers

        if "quantos clientes" in text:


            self.logger.info(
                "[ANALYSIS_AGENT] Operation: count customers"
            )


            customers = self.repository.get(
                "customers"
            )


            result = self.statistics_engine.count_rows(
                customers
            )


            self.logger.info(
                f"[ANALYSIS_AGENT] Customers count result: {result}"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "customers",

                "result": result

            }



        # Product columns

        if "colunas" in text:


            self.logger.info(
                "[ANALYSIS_AGENT] Operation: get columns"
            )


            products = self.repository.get(
                "products"
            )


            result = self.statistics_engine.columns(
                products
            )


            return {

                "type": "analysis",

                "operation": "columns",

                "dataset": "products",

                "result": result

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


            self.logger.info(
                "[ANALYSIS_AGENT] Operation: category frequency"
            )


            products = self.repository.get(
                "products"
            )


            result = self.statistics_engine.value_counts(
                products,
                "product_category_name",
                limit=5
            )


            return {

                "type": "analysis",

                "operation": "value_counts",

                "dataset": "products",

                "column": "product_category_name",

                "result": result

            }



        self.logger.warning(
            "[ANALYSIS_AGENT] Unknown analytical question."
        )


        return {

            "type": "analysis",

            "operation": "unknown",

            "result": "Pergunta analítica não reconhecida."

        }