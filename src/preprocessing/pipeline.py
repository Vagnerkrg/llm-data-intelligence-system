import pandas as pd

from src.preprocessing.cleaner import DataCleaner
from src.preprocessing.transformer import DataTransformer


class PreprocessingPipeline:
    """
    Orchestrates preprocessing stages.

    Executes cleaning and transformation steps
    in a controlled pipeline.
    """


    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()



    def run(self):
        """
        Executes the preprocessing pipeline.

        Flow:

        DataFrame
            |
            v
        DataCleaner
            |
            v
        DataTransformer
            |
            v
        Processed DataFrame
        """

        cleaner = DataCleaner(self.df)

        cleaned_df = cleaner.clean()


        transformer = DataTransformer(cleaned_df)

        transformed_df = transformer.transform()


        return transformed_df