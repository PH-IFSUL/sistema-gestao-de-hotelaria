
from typing import List, Optional
from models.room.room import Quarto

class InMemoryRoomRepository:
    def __init__(self):
        self._quartos: List[Quarto] = []
        self._tipos: List[str] = []

    def add(self, quarto: Quarto) -> None:
        if self.find_by_number(quarto.get_numero()):
            raise ValueError(f"Já existe um quarto com o"
                             f" número {quarto.get_numero()}.")
        self._quartos.append(quarto)

    def list(self) -> list[Quarto]:
        return list(self._quartos)

    def find_by_number(self, number_query: int) -> Optional[Quarto]:
        for q in self._quartos:
            if q.get_numero() == number_query:
                return q
        return None

    def delete(self, number_query: int) -> bool:
        quarto = self.find_by_number(number_query)
        if quarto:
            self._quartos.remove(quarto)
            return True
        return False

    def get_types(self) -> List[str]:
        for quarto in self._quartos:
            self._tipos.append(quarto.get_tipo())
        return list(list(self._tipos))