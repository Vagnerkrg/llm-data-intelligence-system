from abc import ABC, abstractmethod

from src.agents.tools.tool_metadata import ToolMetadata


class BaseTool(ABC):
    """
    Base interface for agent tools.

    Every tool integrated with the Agent System
    must implement this contract.
    """


    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool identifier.
        """
        pass



    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable tool description.
        """
        pass



    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """
        Tool metadata information.
        """
        pass



    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute tool operation.

        Each specialized tool must implement
        its own execution logic.
        """
        pass