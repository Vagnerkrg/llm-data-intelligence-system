from pathlib import Path
import pandas as pd


class OlistDataLoader:
    """
    Responsável pelo carregamento dos dados brutos do dataset Olist.

    Este módulo não modifica os arquivos originais.
    Apenas realiza leitura e disponibiliza os dados para as próximas etapas.
    """

    def __init__(self, data_path="data/raw/olist"):
        self.data_path = Path(data_path)


    def load_csv(self, filename):
        """
        Carrega um arquivo CSV específico do dataset.
        """

        file_path = self.data_path / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {file_path}"
            )

        return pd.read_csv(file_path)


    def load_all(self):
        """
        Carrega os principais arquivos do dataset Olist.
        """

        datasets = {
            "customers": "olist_customers_dataset.csv",
            "orders": "olist_orders_dataset.csv",
            "order_items": "olist_order_items_dataset.csv",
            "products": "olist_products_dataset.csv",
            "payments": "olist_order_payments_dataset.csv",
            "reviews": "olist_order_reviews_dataset.csv",
            "sellers": "olist_sellers_dataset.csv",
            "geolocation": "olist_geolocation_dataset.csv"
        }

        data = {}

        for name, filename in datasets.items():
            data[name] = self.load_csv(filename)

        return data