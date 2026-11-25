from datetime import date
from typing import List, Optional
from ...estadia import Reserva


class ReservaRepositorioMemoria:
    """Implementação em memória da interface ReservaRepositorio."""

    def __init__(self) -> None:
        self._reservas: list[Reserva] = []
        self._proximo_id: int = 1

    def salvar(self, reserva: Reserva) -> None:
        reserva.id = self._proximo_id
        self._proximo_id += 1
        self._reservas.append(reserva)

    def atualizar(self, reserva: Reserva) -> bool:
        if reserva.id is None:
            return False
        for i, existente in enumerate(self._reservas):
            if existente.id == reserva.id:
                self._reservas[i] = reserva
                return True
        return False

    def remover(self, id_reserva: int) -> bool:
        reserva = self.buscar_por_id(id_reserva)
        if reserva is None:
            return False
        self._reservas.remove(reserva)
        return True

    def listar(self) -> List[Reserva]:
        return list(self._reservas)

    def buscar_por_id(self, id_reserva: int) -> Optional[Reserva]:
        for reserva in self._reservas:
            if reserva.id == id_reserva:
                return reserva
        return None

    def existe_conflito(
        self,
        numero_quarto: int,
        data_inicio: date,
        data_fim: date,
        ignorar_id: int | None = None
    ) -> bool:
        for reserva in self._reservas:
            if reserva.status != "CONFIRMADA" or reserva.quarto is None:
                continue
            if ignorar_id is not None and reserva.id == ignorar_id:
                continue
            if reserva.quarto.get_numero() != numero_quarto:
                continue
            if reserva.data_checkin < data_fim and reserva.data_checkout > data_inicio:
                return True
        return False
