from dataclasses import dataclass
from typing import List


@dataclass
class ToolMetadata:
    """
    Metadata describing an agent tool.
    """

    name: str

    description: str

    capabilities: List[str]