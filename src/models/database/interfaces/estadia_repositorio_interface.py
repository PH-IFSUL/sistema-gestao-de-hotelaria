"""
Interface para o repositório de estadias e reservas.
"""
from typing import Protocol, Optional, List
from datetime import date
from ...quarto import Quarto
from ...cliente import Cliente
from ...estadia import Estadia
from ...fatura import Fatura
from ...item import ItemFatura


def obter_proximo_id(repo: "EstadiaRepositorio") -> int:
    return repo.obter_proximo_id()


class EstadiaRepositorio(Protocol):
    """
    Protocolo que define as operações de persistência para Estadia e Reserva.
    """

    @staticmethod
    def obter_proximo_id() -> int:
        ...

    def salvar(self, estadia: Estadia) -> None:
        ...

    def remover(self, id_cliente: int) -> bool:
        ...

    def obter_fatura(self, id_estadia: int) -> Optional[Fatura]:
        ...

    def adicionar_item_fatura(self, id_estadia: int, item: ItemFatura) -> None:
        ...

    def buscar_por_id(self, id_busca: int) -> Optional[Estadia]:
        ...

    def buscar_por_cpf(self, cpf_busca: str) -> Optional[Estadia]:
        ...

    def obter_reservas_por_data(self, data: date) -> List[Estadia]:
        ...

    def atualizar_quarto(self, quarto: Quarto) -> bool:
        ...

    def atualizar_cliente(self, cliente: Cliente) -> bool:
        ...

    # Compatibilidade
    @staticmethod
    def get_next_id() -> int:
        ...

    def save(self, estadia: Estadia) -> None:
        ...

    def delete(self, client_id: int) -> bool:
        ...

    def get_bill(self, id_stay: int) -> Optional[Fatura]:
        ...

    def add_itens_to_bill(self, id_stay: int, item: ItemFatura) -> None:
        ...

    def find_by_cpf(self, cpf_query: str) -> Optional[Estadia]:
        ...

    def get_date_reservations(self, date_query: date) -> List[Estadia]:
        ...

    def update_room(self, room: Quarto) -> bool:
        ...

    def update_client(self, client: Cliente) -> bool:
        ...


# Aliases para compatibilidade
Stay_Repository = EstadiaRepositorio
get_next_id = obter_proximo_id
