import pandas as pd

from src.preprocessing.pipeline import PreprocessingPipeline



def test_pipeline_execution():

    dataframe = pd.DataFrame(
        {
            " Product Name ": [
                " Product A ",
                " Product A "
            ],
            "Created Date": [
                "2026-01-01",
                "2026-01-01"
            ],
            "empty_column": [
                None,
                None
            ]
        }
    )


    pipeline = PreprocessingPipeline(
        dataframe
    )


    result = pipeline.run()


    assert len(result) == 1

    assert "product_name" in result.columns

    assert "created_date" in result.columns

    assert "empty_column" not in result.columns

    assert pd.api.types.is_datetime64_any_dtype(
        result["created_date"]
    )