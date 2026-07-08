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
        Creates analytical summary for products.
        """


        total_products = len(
            dataframe
        )


        categories = (
            dataframe["product_category_name"]
            .dropna()
            .value_counts()
        )


        total_categories = len(
            categories
        )


        category_text = "\n".join(
            [
                f"- {category}: {count} produtos"
                for category, count in categories.head(15).items()
            ]
        )


        average_weight = (
            dataframe["product_weight_g"]
            .dropna()
            .mean()
            if "product_weight_g" in dataframe.columns
            else 0
        )


        return f"""
Tipo de documento:
Resumo analítico de produtos


Fonte:
products


Total de produtos analisados:
{total_products}


Quantidade de categorias:
{total_categories}


Principais categorias:

{category_text}


Peso médio dos produtos:
{average_weight:.2f} gramas


Este documento representa uma visão agregada
do catálogo de produtos do marketplace.
"""



    def build_review_summary(
        self,
        dataframe: pd.DataFrame
    ) -> str:
        """
        Creates analytical summary for reviews.
        """


        total_reviews = len(
            dataframe
        )


        average_score = (
            dataframe["review_score"]
            .mean()
        )


        score_distribution = (
            dataframe["review_score"]
            .value_counts()
            .sort_index()
        )


        distribution_text = "\n".join(
            [
                f"- Nota {score}: {count} avaliações"
                for score, count in score_distribution.items()
            ]
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


Distribuição das notas:

{distribution_text}


Este documento representa uma visão agregada
da satisfação dos clientes.
"""



    def build_order_summary(
        self,
        dataframe: pd.DataFrame
    ) -> str:
        """
        Creates analytical summary for orders.
        """


        total_orders = len(
            dataframe
        )


        status_distribution = (
            dataframe["order_status"]
            .value_counts()
            if "order_status" in dataframe.columns
            else pd.Series()
        )


        status_text = "\n".join(
            [
                f"- {status}: {count} pedidos"
                for status, count in status_distribution.items()
            ]
        )


        delivered_percentage = 0


        if "order_status" in dataframe.columns:

            delivered_count = (
                dataframe["order_status"]
                .eq("delivered")
                .sum()
            )


            if total_orders > 0:

                delivered_percentage = (
                    delivered_count /
                    total_orders *
                    100
                )


        return f"""
Tipo de documento:
Resumo analítico de pedidos


Fonte:
orders


Total de pedidos analisados:
{total_orders}


Distribuição de status:

{status_text}


Percentual de pedidos entregues:
{delivered_percentage:.2f}%


Este documento representa uma visão agregada
do desempenho operacional e logístico
dos pedidos do marketplace.
"""



    def build_customer_summary(
        self,
        dataframe: pd.DataFrame
    ) -> str:
        """
        Creates analytical summary for customers.
        """


        total_customers = len(
            dataframe
        )


        states = (
            dataframe["customer_state"]
            .value_counts()
            .head(10)
            if "customer_state" in dataframe.columns
            else pd.Series()
        )


        state_text = "\n".join(
            [
                f"- {state}: {count} clientes"
                for state, count in states.items()
            ]
        )


        return f"""
Tipo de documento:
Resumo analítico de clientes


Fonte:
customers


Total de clientes:
{total_customers}


Principais estados:

{state_text}


Este documento representa uma visão agregada
dos clientes do marketplace.
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


        if "orders" in datasets:

            summaries.append(
                self.build_order_summary(
                    datasets["orders"]
                )
            )


        if "customers" in datasets:

            summaries.append(
                self.build_customer_summary(
                    datasets["customers"]
                )
            )


        return summaries