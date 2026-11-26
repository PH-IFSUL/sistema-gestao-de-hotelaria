from .item import ItemFatura


class Fatura:
    """
    Classe para gerenciar a fatura e o consumo do cliente.

    Args:
        id_estadia: identificador da estadia correspondente (opcional)

    Returns:
        Objeto do tipo Fatura.
    """

    def __init__(self, id_estadia: int | None = None) -> None:
        self._id_estadia: int | None = id_estadia
        self._itens: list[ItemFatura] = []

    @property
    def id_estadia(self) -> int | None:
        return self._id_estadia

    @id_estadia.setter
    def id_estadia(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id da estadia deve ser número")
        self._id_estadia = value

    def adicionar_item(self, item: ItemFatura) -> None:
        self._itens.append(item)

    def obter_itens(self) -> list[ItemFatura]:
        return list(self._itens)

    def calcular_total(self) -> float:
        return sum(
            item_fatura.item.preco * item_fatura.quantidade
            for item_fatura in self._itens
        )
