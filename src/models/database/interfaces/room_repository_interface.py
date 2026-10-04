'''
    interface com qualquer tipo de Repo (Memória, sql, csv) para o Quarto:
    
        -> todas as implementações tem que ter os mesmos métodos
'''
from typing import Protocol, List, Optional
from ...room.room import Room

class Room_Repository(Protocol):
    '''
    Métodos:
        add(quarto: Room) -> None:
        delete(number_query: int ) -> bool:
        list() -> List[Room]:
        find_by_number(number_query: int) -> Optional[Room]:
        get_types() -> List[str]:
    '''
    
    def add(self, quarto: Room) -> None:
        ...

    def delete(self, number_query: int ) -> bool:
        ...

    def list(self) -> List[Room]:
        ...

    def find_by_number(self, number_query: int) -> Optional[Room]:
        ...
        
    def get_types(self) -> List[str]:
        ...
        
    '''
    def update(self, guest: Room) -> bool:
        ... 
    
    '''