from typing import List, Optional
from ...estadia import Estadia
from ...fatura import Fatura
from ...item import Item, ItemFatura


class EstadiaRepositorioMemoria:
    """Implementação em memória para persistência de estadias e faturas."""

    def __init__(self) -> None:
        self._estadias: list[Estadia] = []
        self._proximo_id: int = 1
        self._proximo_item_fatura_id: int = 1
        self._catalogo: list[Item] = [
            Item(1, "Frigobar", 15.00),
            Item(2, "Lavanderia", 30.00),
            Item(3, "Serviço de Quarto", 25.00),
        ]

    def salvar(self, estadia: Estadia) -> None:
        estadia.id = self._proximo_id
        self._proximo_id += 1
        self._estadias.append(estadia)

    def atualizar(self, estadia: Estadia) -> bool:
        if estadia.id is None:
            return False
        for idx, existente in enumerate(self._estadias):
            if existente.id == estadia.id:
                self._estadias[idx] = estadia
                return True
        return False

    def remover(self, id_estadia: int) -> bool:
        estadia = self.buscar_por_id(id_estadia)
        if estadia is None:
            return False
        self._estadias.remove(estadia)
        return True

    def listar(self) -> List[Estadia]:
        return list(self._estadias)

    def buscar_por_id(self, id_busca: int) -> Optional[Estadia]:
        for estadia in self._estadias:
            if estadia.id == id_busca:
                return estadia
        return None

    def obter_fatura(self, id_estadia: int) -> Optional[Fatura]:
        estadia = self.buscar_por_id(id_estadia)
        return estadia.fatura if estadia is not None else None

    def listar_itens_catalogo(self) -> List[Item]:
        return list(self._catalogo)

    def adicionar_item_fatura(self, id_estadia: int, item: ItemFatura) -> None:
        estadia = self.buscar_por_id(id_estadia)
        if estadia is None:
            raise ValueError(f"Estadia #{id_estadia} não encontrada.")
        item.id = self._proximo_item_fatura_id
        self._proximo_item_fatura_id += 1
        estadia.adicionar_item(item)
