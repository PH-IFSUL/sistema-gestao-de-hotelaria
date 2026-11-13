"""
Interface para o repositório de clientes.
"""
from typing import Protocol, List, Optional
from ...cliente import Cliente


class ClienteRepositorio(Protocol):
    """
    Protocolo que define as operações de persistência para Cliente.
    """

    def salvar(self, cliente: Cliente) -> None:
        """Adiciona ou salva um cliente no repositório."""
        ...

    def remover(self, cpf_cliente: str) -> bool:
        """Remove um cliente pelo CPF."""
        ...

    def obter_todos(self) -> List[Cliente]:
        """Retorna todos os clientes cadastrados."""
        ...

    def buscar_por_id(self, id_busca: int) -> Optional[Cliente]:
        """Busca um cliente pelo identificador único."""
        ...

    def buscar_por_cpf(self, cpf_busca: str) -> Optional[Cliente]:
        """Busca um cliente pelo CPF."""
        ...

    def atualizar(self, cliente: Cliente) -> bool:
        """Atualiza os dados de um cliente."""
        ...

    # Compatibilidade
    def save(self, cliente: Cliente) -> None:
        ...

    def delete(self, client_cpf: str) -> bool:
        ...

    def get_all(self) -> List[Cliente]:
        ...

    def find_by_id(self, id_query: int) -> Optional[Cliente]:
        ...

    def find_by_Cpf(self, cpf_query: str) -> Optional[Cliente]:
        ...

    def update(self, guest: Cliente) -> bool:
        ...


# Alias para compatibilidade
Client_Repository = ClienteRepositorio
