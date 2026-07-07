import pandas as pd


class DataPreprocessor:
    """
    Generic DataFrame preprocessing component.

    Responsible for applying initial transformations
    without modifying the original dataset.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()


    def standardize_columns(self):
        """
        Standardizes column names.
        """

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return self.df


    def convert_datetime_columns(self):
        """
        Converts columns that represent dates
        into datetime format.
        """

        datetime_keywords = [
            "date",
            "timestamp",
            "approved",
            "created",
            "updated",
            "delivered",
            "purchase"
        ]

        for column in self.df.columns:

            column_name = column.lower()

            if any(
                keyword in column_name
                for keyword in datetime_keywords
            ):

                self.df[column] = pd.to_datetime(
                    self.df[column],
                    errors="coerce"
                )

        return self.df


    def clean_text_columns(self):
        """
        Removes unnecessary spaces from text columns.
        """

        for column in self.df.select_dtypes(
            include="object"
        ).columns:

            self.df[column] = (
                self.df[column]
                .str.strip()
            )

        return self.df


    def process(self):
        """
        Executes preprocessing pipeline.
        """

        self.standardize_columns()
        self.convert_datetime_columns()
        self.clean_text_columns()

        return self.df