from typing import Dict, Any


class StatisticsEngine:
    """
    Provides reusable statistical operations
    over project datasets.

    This layer abstracts dataframe operations
    from AI agents.

    V1.0
    - Initial reusable analysis layer.
    - Compatible with Data Analysis Agent.
    - Provides safe analytical operations.
    """



    def count_rows(
        self,
        dataframe
    ) -> int:
        """
        Returns number of records.
        """

        return len(dataframe)



    def columns(
        self,
        dataframe
    ):
        """
        Returns dataframe columns.
        """

        return list(
            dataframe.columns
        )



    def get_column_names(
        self,
        dataframe
    ):
        """
        Returns dataframe column names.

        Compatibility method for
        external consumers and tests.
        """

        return self.columns(
            dataframe
        )



    def summary(
        self,
        dataframe
    ) -> Dict[str, Any]:
        """
        Returns basic dataframe statistics.
        """

        return {

            "rows": len(dataframe),

            "columns": list(
                dataframe.columns
            ),

            "missing_values": (
                dataframe
                .isnull()
                .sum()
                .to_dict()
            )

        }



    def value_counts(
        self,
        dataframe,
        column,
        limit=10
    ):
        """
        Returns most frequent values
        from a column.
        """


        if column not in dataframe.columns:

            return {
                "error": (
                    f"Column not found: {column}"
                )
            }


        return (

            dataframe[column]
            .value_counts()
            .head(limit)
            .to_dict()

        )