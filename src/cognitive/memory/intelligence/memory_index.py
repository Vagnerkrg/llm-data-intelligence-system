from typing import Dict, List, Optional, Any
from uuid import uuid4


class MemoryIndex:
    """
    Índice responsável por organizar memórias
    da camada Memory Intelligence.

    Responsabilidades:

    - gerar identificadores
    - armazenar conteúdos
    - recuperar memórias
    - buscar informações
    """


    def __init__(self):

        self._index: Dict[str, Dict[str, Any]] = {}



    def add(
        self,
        memory_id: Optional[str] = None,
        metadata: Optional[Any] = None
    ) -> str:
        """
        Adiciona uma memória ao índice.

        Caso o identificador não seja informado,
        um novo ID é criado.
        """

        if memory_id is None:

            memory_id = str(
                uuid4()
            )


        if isinstance(metadata, dict):

            stored_data = metadata

        else:

            stored_data = {
                "content": metadata
            }


        self._index[memory_id] = stored_data


        return memory_id



    def get(
        self,
        memory_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Recupera uma memória pelo ID.
        """

        return self._index.get(
            memory_id
        )



    def exists(
        self,
        memory_id: str
    ) -> bool:
        """
        Verifica existência da memória.
        """

        return memory_id in self._index



    def remove(
        self,
        memory_id: str
    ) -> bool:
        """
        Remove uma memória.
        """

        if memory_id not in self._index:

            return False


        del self._index[memory_id]


        return True



    def list_ids(
        self
    ) -> List[str]:
        """
        Lista identificadores armazenados.
        """

        return list(
            self._index.keys()
        )



    def count(
        self
    ) -> int:
        """
        Retorna quantidade de memórias.
        """

        return len(
            self._index
        )