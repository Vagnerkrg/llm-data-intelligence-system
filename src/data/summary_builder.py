from typing import Dict, List

import pandas as pd



class SummaryBuilder:
    """
    Creates analytical summary documents from datasets.

    These documents provide aggregated knowledge
    for RAG business questions.
    """



    def build_product_summary(
        self,
        dataframe: pd.DataFrame
    ) -> str:
        """
        Creates a summary document for products dataset.
        """


        total_products = len(
            dataframe
        )


        categories = (
            dataframe["product_category_name"]
            .dropna()
            .value_counts()
            .head(10)
        )


        category_text = "\n".join(
            [
                f"- {category}: {count} produtos"
                for category, count in categories.items()
            ]
        )


        return f"""
Tipo de documento:
Resumo analítico de produtos


Fonte:
products


Total de produtos analisados:
{total_products}


Principais categorias:

{category_text}


Este documento representa uma visão agregada
do catálogo de produtos do marketplace.
"""



    def build_review_summary(
        self,
        dataframe: pd.DataFrame
    ) -> str:
        """
        Creates a summary document for reviews dataset.
        """


        total_reviews = len(
            dataframe
        )


        average_score = (
            dataframe["review_score"]
            .mean()
        )


        return f"""
Tipo de documento:
Resumo analítico de avaliações


Fonte:
reviews


Total de avaliações:
{total_reviews}


Média das avaliações:
{average_score:.2f}


Este documento representa uma visão agregada
da satisfação dos clientes.
"""



    def build_dataset_summaries(
        self,
        datasets: Dict[str, pd.DataFrame]
    ) -> List[str]:
        """
        Generates summary documents
        from available datasets.
        """


        summaries = []


        if "products" in datasets:

            summaries.append(
                self.build_product_summary(
                    datasets["products"]
                )
            )


        if "reviews" in datasets:

            summaries.append(
                self.build_review_summary(
                    datasets["reviews"]
                )
            )


        return summaries