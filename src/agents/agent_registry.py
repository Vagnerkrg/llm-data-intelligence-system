from typing import Dict, Any, List

from src.agents.tools.base_tool import BaseTool
from src.agents.tools.tool_metadata import ToolMetadata


class AgentRegistry:
    """
    Registry responsible for managing agents and tools.

    Provides centralized discovery of components
    available to the agent execution layer.
    """


    def __init__(self):

        self._registry: Dict[str, Any] = {}



    def register(
        self,
        name: str,
        component: Any
    ):
        """
        Register an agent or tool.
        """

        self._registry[name] = component



    def register_tool(
        self,
        tool: BaseTool
    ):
        """
        Register an agent tool using
        the tool contract.
        """

        self._registry[tool.name] = tool



    def get(
        self,
        name: str
    ):
        """
        Retrieve a registered component.
        """

        return self._registry.get(name)



    def get_tool(
        self,
        name: str
    ):
        """
        Retrieve a registered tool.
        """

        component = self._registry.get(name)


        if isinstance(
            component,
            BaseTool
        ):

            return component


        return None



    def list_components(self):
        """
        Return all registered components.
        """

        return list(
            self._registry.keys()
        )



    def list_tools(self):
        """
        Return only registered tools.
        """

        return [

            name

            for name, component in self._registry.items()

            if isinstance(
                component,
                BaseTool
            )

        ]



    def list_tool_metadata(
        self
    ) -> List[ToolMetadata]:
        """
        Return metadata from all registered tools.
        """

        return [

            tool.metadata

            for tool in self._registry.values()

            if isinstance(
                tool,
                BaseTool
            )

        ]



    def find_tools_by_capability(
        self,
        capability: str
    ) -> List[BaseTool]:
        """
        Find registered tools that support
        a specific capability.
        """

        return [

            tool

            for tool in self._registry.values()

            if isinstance(
                tool,
                BaseTool
            )

            and capability in tool.metadata.capabilities

        ]