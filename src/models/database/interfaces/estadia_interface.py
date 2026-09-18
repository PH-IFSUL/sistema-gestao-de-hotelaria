from typing import Protocol, List, Optional
from ...client.estadia import Estadia
from ...product.produto import Produto

class EstadiaRepository(Protocol):

    def get_next_id(self) -> int:
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

    def get_chekin_date(self, guest: Cliente) -> bool:
        ... 
    
    def update_chekin_date(self, guest: Cliente) -> bool:
        ... 

    def get_chekout_date(self, guest: Cliente) -> bool:
        ... 

    def update_chekout_date(self, guest: Cliente) -> bool:
            ... 