from typing import List, Optional
from ...cliente import Cliente


class ClienteRepositorioMemoria:
    """
    Implementação em memória da interface de repositório de clientes.
    """

    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._proximo_id: int = 1

    def atualizar_proximo_id(self) -> None:
        self._proximo_id = len(self._clientes) + 1

    def salvar(self, cliente: Cliente) -> None:
        if self.buscar_por_cpf(cliente.get_cpf()):
            raise ValueError(f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        cliente.set_id(self._proximo_id)
        self._clientes.append(cliente)
        self.atualizar_proximo_id()

    def remover(self, cpf_cliente: str) -> bool:
        cliente = self.buscar_por_cpf(cpf_cliente)
        if cliente:
            self._clientes.remove(cliente)
            return True
        return False

    def obter_todos(self) -> List[Cliente]:
        return list(self._clientes)

    def buscar_por_id(self, id_busca: int) -> Optional[Cliente]:
        for c in self._clientes:
            if c.get_id() == id_busca:
                return c
        return None

    def buscar_por_cpf(self, cpf_busca: str) -> Optional[Cliente]:
        for c in self._clientes:
            if c.get_cpf() == cpf_busca:
                return c
        return None

    def atualizar(self, cliente: Cliente) -> bool:
        existente = self.buscar_por_cpf(cliente.get_cpf())
        if existente:
            indice = self._clientes.index(existente)
            self._clientes[indice] = cliente
            return True
        return False


