from typing import Dict, List

import pandas as pd



class DocumentBuilder:
    """
    Converts structured datasets into semantic documents
    optimized for embedding generation and RAG retrieval.
    """


    def build_from_dataframe(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str,
        limit: int = None
    ) -> List[str]:
        """
        Builds semantic documents from a dataframe.
        """


        documents = []


        if limit:
            dataframe = dataframe.head(limit)


        for _, row in dataframe.iterrows():

            document = self._build_document(
                row,
                dataset_name
            )

            documents.append(
                document
            )


        return documents



    def build_from_datasets(
        self,
        datasets: Dict[str, pd.DataFrame],
        limit: int = 50
    ) -> List[str]:
        """
        Builds documents from multiple datasets.
        """


        documents = []


        for dataset_name, dataframe in datasets.items():

            dataset_documents = self.build_from_dataframe(
                dataframe,
                dataset_name,
                limit
            )

            documents.extend(
                dataset_documents
            )


        return documents



    def _build_document(
        self,
        row: pd.Series,
        dataset_name: str
    ) -> str:
        """
        Creates a semantic document according to dataset type.
        """


        if dataset_name == "products":

            return self._product_document(row)


        if dataset_name == "reviews":

            return self._review_document(row)


        if dataset_name == "orders":

            return self._order_document(row)


        if dataset_name == "customers":

            return self._customer_document(row)


        return self._generic_document(
            row,
            dataset_name
        )



    def _product_document(
        self,
        row
    ):

        return f"""
Tipo de documento:
Produto

Fonte:
products

Produto cadastrado no marketplace.

Categoria:
{row.get('product_category_name')}

Peso:
{row.get('product_weight_g')} gramas

Dimensões:
Altura: {row.get('product_height_cm')}
Largura: {row.get('product_width_cm')}
Comprimento: {row.get('product_length_cm')}

Este documento representa informações de produtos disponíveis para venda.
"""



    def _review_document(
        self,
        row
    ):

        return f"""
Tipo de documento:
Avaliação de cliente

Fonte:
reviews

Avaliação de compra realizada por cliente.

Nota da avaliação:
{row.get('review_score')}

Comentário:
{row.get('review_comment_message')}

Data da avaliação:
{row.get('review_creation_date')}

Este documento representa uma experiência de pós-venda e satisfação do cliente.
"""



    def _order_document(
        self,
        row
    ):

        return f"""
Tipo de documento:
Pedido

Fonte:
orders

Pedido realizado no marketplace.

Status:
{row.get('order_status')}

Data da compra:
{row.get('order_purchase_timestamp')}

Entrega prevista:
{row.get('order_estimated_delivery_date')}

Entrega realizada:
{row.get('order_delivered_customer_date')}

Este documento representa informações de pedidos e logística.
"""



    def _customer_document(
        self,
        row
    ):

        return f"""
Tipo de documento:
Cliente

Fonte:
customers

Cliente cadastrado no marketplace.

Cidade:
{row.get('customer_city')}

Estado:
{row.get('customer_state')}

Este documento representa informações cadastrais de clientes.
"""



    def _generic_document(
        self,
        row,
        dataset_name
    ):

        information = "\n".join(
            [
                f"{column}: {value}"
                for column, value in row.items()
            ]
        )


        return f"""
Tipo de documento:
Dataset genérico

Fonte:
{dataset_name}

Information:
{information}
"""