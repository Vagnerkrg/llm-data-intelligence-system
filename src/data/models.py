from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class DatasetInfo:
    """
    Metadata information about a dataset.
    """

    name: str
    rows: int
    columns: int


@dataclass
class LoadResult:
    """
    Standard result returned after loading data.
    """

    name: str
    dataframe: pd.DataFrame
    info: DatasetInfo


@dataclass
class DataSource:
    """
    Represents a data source.
    """

    name: str
    path: str
    format: str