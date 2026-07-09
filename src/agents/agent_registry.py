from typing import Dict, Any


class AgentRegistry:
    """
    Registry responsible for managing available agents and tools.
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



    def get(
        self,
        name: str
    ):
        """
        Retrieve a registered component.
        """

        return self._registry.get(name)



    def list_components(self):
        """
        Return available components.
        """

        return list(self._registry.keys())