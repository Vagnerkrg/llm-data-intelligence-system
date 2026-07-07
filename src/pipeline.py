from pathlib import Path

from src.data.data_loader import OlistDataLoader
from src.data.validator import DataValidator
from src.preprocessing.preprocess import DataPreprocessor


class DataPipeline:
    """
    Main data processing pipeline.

    Responsible for orchestrating:
    - data loading
    - data validation
    - preprocessing
    - processed data persistence
    """


    def __init__(
        self,
        data_path="data/raw/olist",
        output_path="data/processed"
    ):
        self.loader = OlistDataLoader(
            data_path=data_path
        )

        self.output_path = Path(
            output_path
        )

        self.output_path.mkdir(
            parents=True,
            exist_ok=True
        )


    def save_processed_data(
        self,
        datasets
    ):
        """
        Saves processed datasets as parquet files.
        """

        for name, dataframe in datasets.items():

            file_path = (
                self.output_path /
                f"{name}.parquet"
            )

            dataframe.to_parquet(
                file_path,
                index=False
            )

            print(
                f"Saved: {file_path}"
            )


    def run(self):
        """
        Executes complete data pipeline.
        """

        print(
            "Starting data pipeline..."
        )


        datasets = self.loader.load_all()


        print(
            f"Loaded datasets: {list(datasets.keys())}"
        )


        processed_data = {}


        for name, dataframe in datasets.items():

            print(
                f"\nProcessing dataset: {name}"
            )


            validator = DataValidator(
                dataframe
            )

            validation_result = (
                validator.validate()
            )


            print(
                f"Rows: {validation_result['summary']['rows']}"
            )


            preprocessor = DataPreprocessor(
                dataframe
            )


            processed_dataframe = (
                preprocessor.process()
            )


            processed_data[name] = (
                processed_dataframe
            )


        self.save_processed_data(
            processed_data
        )


        print(
            "\nData pipeline completed successfully."
        )


        return processed_data



if __name__ == "__main__":

    pipeline = DataPipeline()

    data = pipeline.run()


    print(
        "\nAvailable processed datasets:"
    )

    print(
        list(data.keys())
    )