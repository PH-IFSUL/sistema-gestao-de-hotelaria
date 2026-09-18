from __future__ import annotations
from typing import Protocol, List, Optional
from ...client.estadia import Estadia
from ...product.produto import Produto
from datetime import date

def get_next_id(repo: EstadiaRepository) -> int:
    return repo.get_next_id()


class EstadiaRepository(Protocol):

    @staticmethod
    def get_next_id() -> int:
        ...

    def save(self, estadia: Estadia) -> None:
        ...
    
    def delete(self, client_id: int) -> bool:
        ...

    def get_consumos(self) -> List[Produto]:
        ...

    def set_new_consumo(self) -> List[Produto]:
            ...

    def find_by_id(self, id_query: int) -> Optional[Estadia]:
        ...

    def find_by_Cpf(self, cpf_query: str) -> Optional[Estadia]:
        ...
 
    def get_date_reservations(self, date: date) -> list[Estadia]:
        ... 

