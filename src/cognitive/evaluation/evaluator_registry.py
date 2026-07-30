from typing import Dict, Any


class EvaluatorRegistry:
    """
    Registro central dos avaliadores cognitivos.
    """

    def __init__(self):
        self._evaluators: Dict[str, Any] = {}


    def register(
        self,
        name: str,
        evaluator: Any
    ) -> None:

        self._evaluators[name] = evaluator


    def get(
        self,
        name: str
    ) -> Any:

        return self._evaluators.get(name)


    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._evaluators


    def list_evaluators(self):

        return list(
            self._evaluators.keys()
        )