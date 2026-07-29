from typing import Dict, List, Optional, Any


class MemoryIndex:
    """
    Índice responsável por organizar referências
    de conhecimentos armazenados na memória cognitiva.

    A primeira versão trabalha com indexação simples
    por identificadores e metadados.
    """

    def __init__(self):
        self._index: Dict[str, Dict[str, Any]] = {}


    def add(
        self,
        memory_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Adiciona uma memória ao índice.
        """

        if metadata is None:
            metadata = {}

        self._index[memory_id] = metadata



    def get(
        self,
        memory_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Recupera metadados de uma memória.
        """

        return self._index.get(
            memory_id
        )



    def exists(
        self,
        memory_id: str
    ) -> bool:
        """
        Verifica se uma memória está indexada.
        """

        return memory_id in self._index



    def remove(
        self,
        memory_id: str
    ) -> bool:
        """
        Remove uma memória do índice.
        """

        if memory_id not in self._index:
            return False

        del self._index[memory_id]

        return True



    def list_ids(self) -> List[str]:
        """
        Retorna todos os identificadores indexados.
        """

        return list(
            self._index.keys()
        )



    def count(self) -> int:
        """
        Retorna quantidade de memórias indexadas.
        """

        return len(
            self._index
        )