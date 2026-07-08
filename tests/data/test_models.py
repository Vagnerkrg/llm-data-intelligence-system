import pandas as pd

from src.data.models import (
    DataSource,
    DatasetInfo,
    LoadResult
)


def test_datasource_creation():

    source = DataSource(
        name="products",
        path="data/raw/products.csv",
        format="csv"
    )

    assert source.name == "products"
    assert source.path == "data/raw/products.csv"
    assert source.format == "csv"



def test_dataset_info_creation():

    info = DatasetInfo(
        name="products",
        rows=100,
        columns=5
    )

    assert info.name == "products"
    assert info.rows == 100
    assert info.columns == 5



def test_load_result_creation():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20]
        }
    )


    info = DatasetInfo(
        name="test",
        rows=2,
        columns=2
    )


    result = LoadResult(
        name="test",
        dataframe=dataframe,
        info=info
    )


    assert result.name == "test"
    assert isinstance(result.dataframe, pd.DataFrame)
    assert result.info.rows == 2