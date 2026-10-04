from src.models.room import Quarto as Room
from typing import Protocol, Optional
from ...client.stay_info import Guest_Stay
from ...invoice.invoice import Guest_Bill
from ...invoice.itens import Bill_Item
from datetime import date

def get_next_id(repo: EstadiaRepository) -> int:
    return repo.get_next_id()


class EstadiaRepository(Protocol):

    @staticmethod
    def get_next_id() -> int:
        ...

    def save(self, estadia: Guest_Stay) -> None:
        ...
    
    def delete(self, client_id: int) -> bool:
        ...

    def get_bill(self, id_stay: int) -> Optional[Guest_Bill]:
        ...

    def add_itens_to_bill(self, id_stay: int, item: Bill_Item) -> None:
        ...

    def find_by_id(self, id_query: int) -> Optional[Guest_Stay]:
        ...

    def find_by_cpf(self, cpf_query: str) -> Optional[Guest_Stay]:
        ...
 
    def get_date_reservations(self, date: date) -> list[Guest_Stay]:
        ... 

    def update_room(self, id_stay: int, room: Room) -> bool:
        ...

