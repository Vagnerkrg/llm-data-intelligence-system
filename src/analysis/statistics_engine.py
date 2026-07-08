from typing import Dict, Any


class StatisticsEngine:
    """
    Provides reusable statistical operations
    over project datasets.

    This layer abstracts dataframe operations
    from AI agents.
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

            raise ValueError(
                f"Column not found: {column}"
            )


        return (

            dataframe[column]
            .value_counts()
            .head(limit)
            .to_dict()

        )