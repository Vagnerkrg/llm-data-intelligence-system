from typing import Dict

from src.services.data_intelligence_service import DataIntelligenceService
from src.analysis.analytics_engine import AnalyticsEngine
from src.analysis.dataframe_repository import DataFrameRepository
from src.logging import AppLogger



class DataAnalysisAgent:
    """
    Agent responsible for structured data analysis.

    Uses DataIntelligenceService as the primary abstraction layer.

    Maintains backward compatibility with previous
    repository and analytics_engine injection.
    """


    def __init__(
        self,
        intelligence_service=None,
        analytics_engine=None,
        repository=None
    ):


        if intelligence_service:

            self.intelligence = intelligence_service


        else:

            if analytics_engine:

                self.intelligence = DataIntelligenceService(
                    analytics_engine=analytics_engine
                )


            elif repository:

                analytics = AnalyticsEngine(
                    repository=repository
                )

                self.intelligence = DataIntelligenceService(
                    analytics_engine=analytics
                )


            else:

                self.intelligence = DataIntelligenceService()



        self.logger = AppLogger(
            self.__class__.__name__
        )



    def run(
        self,
        question: str
    ) -> Dict:


        self.logger.info(
            f"[ANALYSIS_AGENT] Question received: {question}"
        )


        text = question.lower()



        if "quantos produtos" in text:


            result = self.intelligence.count_dataset_rows(
                "products"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "products",

                "result": result

            }



        if "quantos clientes" in text:


            result = self.intelligence.count_dataset_rows(
                "customers"
            )


            return {

                "type": "analysis",

                "operation": "count_rows",

                "dataset": "customers",

                "result": result

            }



        if "colunas" in text:


            result = self.intelligence.get_dataset_columns(
                "products"
            )


            return {

                "type": "analysis",

                "operation": "columns",

                "dataset": "products",

                "result": result

            }



        if (
            "categoria" in text
            and
            (
                "mais" in text
                or "maior" in text
                or "possui" in text
            )
        ):


            result = self.intelligence.get_value_counts(
                "products",
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



        return {

            "type": "analysis",

            "operation": "unknown",

            "result": "Pergunta analítica não reconhecida."

        }