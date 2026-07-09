from dataclasses import dataclass
from typing import List


@dataclass
class ToolMetadata:
    """
    Metadata describing an agent tool.

    Contains identity, capabilities and
    runtime configuration information.
    """

    name: str

    description: str

    capabilities: List[str]

    version: str = "1.0"

    enabled: bool = True

    priority: int = 0