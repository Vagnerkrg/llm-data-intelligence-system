from typing import Dict, Any, Optional

from .memory_index import MemoryIndex


class LearningMemoryManager:
    """
    Gerenciador de memória cognitiva.

    Responsável por armazenar, recuperar
    e consultar aprendizados.
    """


    def __init__(
        self,
        memory_index: Optional[MemoryIndex] = None
    ):
        """
        Cria o gerenciador.

        Caso nenhum índice seja informado,
        cria um MemoryIndex interno.
        """

        self.memory_index = (
            memory_index
            if memory_index is not None
            else MemoryIndex()
        )



    def store(
        self,
        memory_id: str,
        content: Any
    ) -> bool:
        """
        Armazena uma memória.
        """

        self.memory_index.add(
            memory_id,
            content
        )

        return True



    def store_learning(
        self,
        memory_id: str,
        learning: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Armazena aprendizado cognitivo.
        """

        self.store(
            memory_id,
            learning
        )

        return {
            "stored": True,
            "memory_id": memory_id,
            "learning": learning
        }



    def retrieve(
        self,
        memory_id: str
    ) -> Optional[Any]:
        """
        Recupera memória.
        """

        return self.memory_index.get(
            memory_id
        )



    def retrieve_learning(
        self,
        memory_id: str
    ) -> Optional[Any]:
        """
        Recupera aprendizado.
        """

        return self.retrieve(
            memory_id
        )



    def exists(
        self,
        memory_id: str
    ) -> bool:
        """
        Verifica existência.
        """

        return self.memory_index.exists(
            memory_id
        )



    def has_learning(
        self,
        memory_id: str
    ) -> bool:
        """
        Alias semântico.
        """

        return self.exists(
            memory_id
        )



    def count(self) -> int:
        """
        Retorna quantidade de memórias.
        """

        return self.memory_index.count()