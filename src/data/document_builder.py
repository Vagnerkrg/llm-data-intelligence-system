from typing import Dict, List

import pandas as pd



class DocumentBuilder:
    """
    Converts structured datasets into semantic documents
    with metadata for RAG retrieval.
    """



    def build_from_dataframe(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str,
        limit: int = None
    ) -> List[Dict]:
        """
        Builds semantic documents with metadata.
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
    ) -> List[Dict]:
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
        row,
        dataset_name
    ):

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




    def _create_document(
        self,
        text,
        source,
        document_type
    ):

        return {
            "text": text,
            "metadata": {
                "source": source,
                "type": document_type
            }
        }




    def _product_document(
        self,
        row
    ):

        text = f"""
Produto cadastrado no marketplace.

Categoria:
{row.get('product_category_name')}

Peso:
{row.get('product_weight_g')} gramas

Dimensões:
Altura: {row.get('product_height_cm')}
Largura: {row.get('product_width_cm')}
Comprimento: {row.get('product_length_cm')}
"""


        return self._create_document(
            text,
            "products",
            "product"
        )




    def _review_document(
        self,
        row
    ):

        text = f"""
Avaliação de compra realizada por cliente.

Nota:
{row.get('review_score')}

Comentário:
{row.get('review_comment_message')}
"""


        return self._create_document(
            text,
            "reviews",
            "review"
        )




    def _order_document(
        self,
        row
    ):

        text = f"""
Pedido realizado no marketplace.

Status:
{row.get('order_status')}

Compra:
{row.get('order_purchase_timestamp')}
"""


        return self._create_document(
            text,
            "orders",
            "order"
        )




    def _customer_document(
        self,
        row
    ):

        text = f"""
Cliente cadastrado no marketplace.

Cidade:
{row.get('customer_city')}

Estado:
{row.get('customer_state')}
"""


        return self._create_document(
            text,
            "customers",
            "customer"
        )




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


        return self._create_document(
            information,
            dataset_name,
            "generic"
        )