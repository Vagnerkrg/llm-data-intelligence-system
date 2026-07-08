import pandas as pd

from src.preprocessing.cleaner import DataCleaner



def test_clean_text_columns():

    dataframe = pd.DataFrame(
        {
            "name": [
                " Product A ",
                " Product B "
            ]
        }
    )


    cleaner = DataCleaner(dataframe)

    result = cleaner.clean_text_columns()


    assert result["name"].iloc[0] == "Product A"



def test_remove_empty_columns():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "empty": [None, None]
        }
    )


    cleaner = DataCleaner(dataframe)

    result = cleaner.remove_empty_columns()


    assert "empty" not in result.columns



def test_remove_duplicates():

    dataframe = pd.DataFrame(
        {
            "id": [1, 1, 2]
        }
    )


    cleaner = DataCleaner(dataframe)

    result = cleaner.remove_duplicates()


    assert len(result) == 2



def test_clean_pipeline():

    dataframe = pd.DataFrame(
        {
            "name": [
                " A ",
                " A "
            ],
            "empty": [
                None,
                None
            ]
        }
    )


    cleaner = DataCleaner(dataframe)

    result = cleaner.clean()


    assert len(result) == 1
    assert "empty" not in result.columns