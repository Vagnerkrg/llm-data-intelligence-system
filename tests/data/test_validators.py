import pandas as pd

from src.data.validator import DataValidator



def test_validator_summary():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "price": [10.0, 20.0, 30.0]
        }
    )

    validator = DataValidator(dataframe)

    summary = validator.summary()

    assert summary["rows"] == 3
    assert summary["columns"] == 2
    assert "memory_usage_mb" in summary



def test_validator_missing_values():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "price": [10.0, None, 30.0]
        }
    )

    validator = DataValidator(dataframe)

    missing = validator.missing_values()

    assert missing["price"] == 1
    assert missing["id"] == 0



def test_validator_data_types():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["A", "B"]
        }
    )

    validator = DataValidator(dataframe)

    types = validator.data_types()

    assert "id" in types
    assert "name" in types



def test_validator_complete_report():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [100, 200]
        }
    )

    validator = DataValidator(dataframe)

    report = validator.validate()

    assert "summary" in report
    assert "missing_values" in report
    assert "data_types" in report