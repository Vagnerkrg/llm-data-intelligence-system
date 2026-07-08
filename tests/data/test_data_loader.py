import pandas as pd
import pytest

from src.data.data_loader import OlistDataLoader
from src.data.models import LoadResult



def test_load_csv_returns_dataframe(tmp_path):

    csv_file = tmp_path / "products.csv"

    dataframe = pd.DataFrame(
        {
            "product_id": ["1", "2"],
            "price": [100, 200]
        }
    )

    dataframe.to_csv(
        csv_file,
        index=False
    )


    loader = OlistDataLoader(
        data_path=tmp_path
    )


    result = loader.load_csv(
        "products.csv",
        name="products"
    )


    assert isinstance(result, LoadResult)
    assert isinstance(result.dataframe, pd.DataFrame)
    assert result.name == "products"
    assert result.info.rows == 2



def test_load_csv_file_not_found(tmp_path):

    loader = OlistDataLoader(
        data_path=tmp_path
    )


    with pytest.raises(FileNotFoundError):

        loader.load_csv(
            "not_found.csv"
        )



def test_load_all_returns_datasets(tmp_path):

    files = {
        "olist_customers_dataset.csv": {
            "customer_id": ["1"]
        },
        "olist_orders_dataset.csv": {
            "order_id": ["1"]
        },
        "olist_order_items_dataset.csv": {
            "order_id": ["1"]
        },
        "olist_products_dataset.csv": {
            "product_id": ["1"]
        },
        "olist_order_payments_dataset.csv": {
            "order_id": ["1"]
        },
        "olist_order_reviews_dataset.csv": {
            "review_id": ["1"]
        },
        "olist_sellers_dataset.csv": {
            "seller_id": ["1"]
        },
        "olist_geolocation_dataset.csv": {
            "zip_code_prefix": ["1"]
        }
    }


    for filename, data in files.items():

        pd.DataFrame(data).to_csv(
            tmp_path / filename,
            index=False
        )


    loader = OlistDataLoader(
        data_path=tmp_path
    )


    result = loader.load_all()


    assert "products" in result
    assert isinstance(
        result["products"],
        LoadResult
    )