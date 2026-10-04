
from typing import List, Optional
from ...client.client import Client

'''
    Classe temporaria para salvar o cliente na memória

'''
class In_Memory_Client_Repository:
    '''
    Classe para salvar os clientes na memória.
    Implementa a interface ClientRepository.

    Métodos:
        __init__() -> None:
        update_next_id() -> None:
        save(cliente: Cliente) -> None:
        delete(client_cpf: str) -> bool:
        get_all() -> List[Cliente]:
        find_by_id(id_query: int) -> Optional[Cliente]:
        find_by_Cpf(cpf_query: str) -> Optional[Cliente]:
    '''

    def __init__(self):
        self._clients: list[Client] = []
        self.__next_id: int = 0

    def update_next_id(self) -> None:
        self.__next_id: int = len(self._clients) +1

    def save(self, cliente: Client) -> None:
        if self.find_by_Cpf(cliente.get_cpf()):
            raise ValueError(f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        cliente._id = self.__next_id
        self.update_next_id()
        self._clients.append(cliente)

    def delete(self, client_cpf: str) -> bool:
        cliente = self.find_by_Cpf(client_cpf)
        if cliente:
            self._clients.remove(cliente)
            return True
        return False

    def get_all(self) -> List[Client]:
        return list(self._clients)
        
    def find_by_id(self, id_query: int) -> Optional[Client]:
        for c in self._clients:
            if c.get_id() == id_query:
                return c
        return None

    def find_by_Cpf(self, cpf_query: str) -> Client | None:
        for c in self._clients:
            if c.get_cpf() == cpf_query:
                return c
        return None

        