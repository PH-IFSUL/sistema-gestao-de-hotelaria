"""
Interface para o repositório de quartos.
"""
from typing import Protocol, List, Optional
from ...quarto import Quarto


class QuartoRepositorio(Protocol):
    """
    Protocolo que define as operações de persistência para Quarto.
    """

    def adicionar(self, quarto: Quarto) -> None:
        """Adiciona um quarto ao repositório."""
        ...

    def remover(self, numero_busca: int) -> bool:
        """Remove um quarto pelo número."""
        ...

    def listar(self) -> List[Quarto]:
        """Retorna a lista de todos os quartos."""
        ...

    def buscar_por_numero(self, numero_busca: int) -> Optional[Quarto]:
        """Busca um quarto pelo seu número."""
        ...

    def obter_tipos(self) -> List[str]:
        """Retorna os tipos de quartos disponíveis."""
        ...

    def atualizar_estado(self, quarto: Quarto) -> bool:
        """Persiste o estado atual do quarto."""
        ...


