import pandas as pd


class DataValidator:
    """
    Generic DataFrame validator.

    Responsible for performing basic checks
    before the next stages of the data pipeline.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe


    def summary(self):
        """
        Returns general dataset information.
        """

        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "memory_usage_mb": float(
                round(
                    self.df.memory_usage(deep=True).sum() / 1024**2,
                    2
                )
            )
        }


    def missing_values(self):
        """
        Returns the amount of missing values.
        """

        return (
            self.df.isnull()
            .sum()
            .sort_values(ascending=False)
        )


    def data_types(self):
        """
        Returns column data types.
        """

        return self.df.dtypes


    def validate(self):
        """
        Executes main validation checks.
        """

        return {
            "summary": self.summary(),
            "missing_values": self.missing_values(),
            "data_types": self.data_types()
        }