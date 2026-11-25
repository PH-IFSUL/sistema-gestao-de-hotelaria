"""
Interface para o repositório de reservas.
"""
from datetime import date
from typing import List, Optional, Protocol
from ...estadia import Reserva


class ReservaRepositorio(Protocol):
    """Protocolo que define as operações de persistência para Reserva."""

    def salvar(self, reserva: Reserva) -> None:
        """Adiciona uma nova reserva ao repositório."""
        ...

    def atualizar(self, reserva: Reserva) -> bool:
        """Atualiza uma reserva existente."""
        ...

    def remover(self, id_reserva: int) -> bool:
        """Remove uma reserva pelo seu ID."""
        ...

    def listar(self) -> List[Reserva]:
        """Retorna todas as reservas cadastradas."""
        ...

    def buscar_por_id(self, id_reserva: int) -> Optional[Reserva]:
        """Busca uma reserva pelo identificador único."""
        ...

    def existe_conflito(
        self,
        numero_quarto: int,
        data_inicio: date,
        data_fim: date,
        ignorar_id: int | None = None
    ) -> bool:
        """Verifica se há conflito de datas para um quarto em reservas confirmadas."""
        ...
