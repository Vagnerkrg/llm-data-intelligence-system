from typing import List, Optional

from .memory_index import MemoryIndex


class KnowledgeRetriever:
    """
    Responsável por recuperar conhecimentos
    armazenados no sistema de memória cognitiva.

    A primeira versão utiliza busca simples
    baseada em metadados indexados.
    """

    def __init__(
        self,
        memory_index: MemoryIndex
    ):
        self.memory_index = memory_index



    def retrieve(
        self,
        memory_id: str
    ) -> Optional[dict]:
        """
        Recupera um conhecimento específico.
        """

        return self.memory_index.get(
            memory_id
        )



    def search(
        self,
        key: str,
        value: str
    ) -> List[dict]:
        """
        Busca conhecimentos por metadados.
        """

        results = []

        for memory_id in self.memory_index.list_ids():

            metadata = self.memory_index.get(
                memory_id
            )

            if metadata is None:
                continue


            if metadata.get(key) == value:

                results.append(
                    {
                        "memory_id": memory_id,
                        "metadata": metadata
                    }
                )


        return results



    def exists(
        self,
        memory_id: str
    ) -> bool:
        """
        Verifica existência de conhecimento.
        """

        return self.memory_index.exists(
            memory_id
        )