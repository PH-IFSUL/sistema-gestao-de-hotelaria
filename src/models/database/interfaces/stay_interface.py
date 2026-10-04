from typing import Protocol, Optional
from ...room.room import Room
from ...client.client import Client
from ...client.stay_info import Guest_Stay
from ...invoice.invoice import Guest_Bill
from ...invoice.itens import Bill_Item
from datetime import date

def get_next_id(repo: Stay_Repository) -> int:
    return repo.get_next_id()


class Stay_Repository(Protocol):
    '''
    Métodos:
        get_next_id() -> int:
        save(estadia: Guest_Stay) -> None:
        delete(client_id: int) -> bool:
        get_bill(id_stay: int) -> Optional[Guest_Bill]:
        add_itens_to_bill(id_stay: int, item: Bill_Item) -> None:
        find_by_id(id_query: int) -> Optional[Guest_Stay]:
        find_by_cpf(cpf_query: str) -> Optional[Guest_Stay]:
        get_date_reservations(date: date) -> list[Guest_Stay]:
        update_room(room: Room) -> bool:
        update_client(client: Client) -> bool:
        update_room(id_stay: int, room: Room) -> bool:
    '''

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

    def update_room(self, room: Room) -> bool:
        ...
    def update_client(self, client: Client) -> bool:
        ...
