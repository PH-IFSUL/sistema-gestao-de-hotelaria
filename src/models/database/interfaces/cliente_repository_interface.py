'''
    interface com qualquer tipo de Repo (Memória, sql, csv) para o cliente:
    
        -> todas as implementações tem que ter os mesmos métodos
'''
from typing import Protocol, List, Optional
from ...guest.cliente import Cliente


class ClientRepository(Protocol):

    def save(self, cliente: Cliente) -> None:
        ...

    # @ fix -> remover por id
    def delete(self, client_cpf: str) -> bool:
        ...

    def get_all(self) -> List[Cliente]:
        ...

    def find_by_id(self, id_query: int) -> Optional[Cliente]:
        ...

    def find_by_Cpf(self, cpf_query: str) -> Optional[Cliente]:
        ...
    """ 
    def update(self, guest: Cliente) -> bool:
        ... """

    