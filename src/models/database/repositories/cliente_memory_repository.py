
from typing import List, Optional
from ...guest.cliente import Cliente

'''
    Classe temporaria para salvar o cliente na memória

'''
class InMemoryCliente:

    def __init__(self):
        self._clientes: list[Cliente] = []
        self.__next_id: int = 0

    def update_next_id(self) -> None:
        self.__next_id: int = len(self._clientes) +1

    def save(self, cliente: Cliente) -> None:
        if self.find_by_Cpf(cliente.get_cpf()):
            raise ValueError(f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        cliente._id = self.__next_id
        self.update_next_id()
        self._clientes.append(cliente)

    def delete(self, client_cpf: str) -> bool:
        cliente = self.find_by_Cpf(client_cpf)
        if cliente:
            self._clientes.remove(cliente)
            return True
        return False

    def get_all(self) -> List[Cliente]:
        return list(self._clientes)
        
    def find_by_id(self, id_query: int) -> Optional[Cliente]:
        for c in self._clientes:
            if c.get_id() == id_query:
                return c
        return None

    def find_by_Cpf(self, cpf_query: str) -> Cliente | None:
        for c in self._clientes:
            if c.get_cpf() == cpf_query:
                return c
        return None

        