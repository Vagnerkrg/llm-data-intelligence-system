import pandas as pd


class DataTransformer:
    """
    Responsible for transforming DataFrames.

    Applies structural transformations without
    modifying the original dataset.
    """


    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()



    def standardize_columns(self):
        """
        Standardizes column names.

        Example:
        "Product Name" -> "product_name"
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



    def transform(self):
        """
        Executes transformation pipeline.
        """

        self.standardize_columns()
        self.convert_datetime_columns()

        return self.df