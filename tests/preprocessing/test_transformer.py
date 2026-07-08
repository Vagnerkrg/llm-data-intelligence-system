import pandas as pd

from src.preprocessing.transformer import DataTransformer



def test_standardize_columns():

    dataframe = pd.DataFrame(
        {
            " Product Name ": ["A"],
            "Price Value": [100]
        }
    )


    transformer = DataTransformer(dataframe)

    result = transformer.standardize_columns()


    assert "product_name" in result.columns
    assert "price_value" in result.columns



def test_convert_datetime_columns():

    dataframe = pd.DataFrame(
        {
            "created_date": [
                "2026-01-01",
                "2026-01-02"
            ]
        }
    )


    transformer = DataTransformer(dataframe)

    result = transformer.convert_datetime_columns()


    assert pd.api.types.is_datetime64_any_dtype(
        result["created_date"]
    )



def test_transform_pipeline():

    dataframe = pd.DataFrame(
        {
            "Created Date": [
                "2026-01-01"
            ],
            " Product Name ": [
                "A"
            ]
        }
    )


    transformer = DataTransformer(dataframe)

    result = transformer.transform()


    assert "created_date" in result.columns
    assert "product_name" in result.columns