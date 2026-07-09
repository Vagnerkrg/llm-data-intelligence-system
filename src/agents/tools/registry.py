from typing import Dict, List

from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata


class ToolRegistry:
    """
    Registry responsible exclusively
    for managing agent tools.
    """

    def __init__(self):

        self._tools: Dict[str, BaseTool] = {}



    def register_tool(
        self,
        tool: BaseTool
    ):
        """
        Register an agent tool.
        """

        self._tools[tool.name] = tool



    def get_tool(
        self,
        name: str
    ):
        """
        Retrieve a registered tool.
        """

        return self._tools.get(name)



    def list_tools(
        self
    ):
        """
        Return all registered tool names.
        """

        return list(
            self._tools.keys()
        )



    def list_active_tools(
        self
    ) -> List[BaseTool]:
        """
        Return only enabled tools.
        """

        return [

            tool

            for tool in self._tools.values()

            if tool.metadata.enabled

        ]



    def list_tool_metadata(
        self
    ) -> List[ToolMetadata]:
        """
        Return metadata from all tools.
        """

        return [

            tool.metadata

            for tool in self._tools.values()

        ]



    def find_tools_by_capability(
        self,
        capability: str
    ) -> List[BaseTool]:
        """
        Find tools supporting
        a capability.
        """

        return [

            tool

            for tool in self._tools.values()

            if capability in tool.metadata.capabilities

        ]



    def find_active_tools_by_capability(
        self,
        capability: str
    ) -> List[BaseTool]:
        """
        Find enabled tools supporting
        a capability.
        """

        return [

            tool

            for tool in self.list_active_tools()

            if capability in tool.metadata.capabilities

        ]