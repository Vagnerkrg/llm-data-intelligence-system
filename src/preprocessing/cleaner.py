import pandas as pd


class DataCleaner:
    """
    Responsible for cleaning raw DataFrames.

    This component does not modify the original dataset.
    It creates a copy before applying transformations.
    """


    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()


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


    def remove_empty_columns(self):
        """
        Removes columns with all values missing.
        """

        self.df = self.df.dropna(
            axis=1,
            how="all"
        )

        return self.df


    def remove_duplicates(self):
        """
        Removes duplicated rows.
        """

        self.df = self.df.drop_duplicates()

        return self.df


    def clean(self):
        """
        Executes cleaning pipeline.
        """

        self.clean_text_columns()
        self.remove_empty_columns()
        self.remove_duplicates()

        return self.df