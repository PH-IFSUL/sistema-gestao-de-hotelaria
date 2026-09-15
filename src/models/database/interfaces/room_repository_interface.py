'''
    interface com qualquer tipo de Repo (Memória, sql, csv) para o Quarto:
    
        -> todas as implementações tem que ter os mesmos métodos
'''
from typing import Protocol, List, Optional
from models.room.room import Quarto

class RoomRepository(Protocol):

    def add(self, quarto: Quarto) -> None:
        ...

    def delete(self, number_query: int ) -> bool:
        ...

    def list(self) -> List[Quarto]:
        ...

    def find_by_number(self, number_query: int) -> Optional[Quarto]:
        ...
        
    def get_types(self) -> List[str]:
        ...
        
    '''
    def update(self, guest: Quarto) -> bool:
        ... 
    
    '''