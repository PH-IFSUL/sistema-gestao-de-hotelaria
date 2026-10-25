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
        if value is None:
            raise ValueError("id da estadia não pode ser vazio")
        self._id_estadia = value

    # Compatibilidade
    @property
    def id_stay(self) -> int | None:
        return self._id_estadia

    @id_stay.setter
    def id_stay(self, value: int) -> None:
        self.id_estadia = value

    @property
    def itens(self) -> list[ItemFatura]:
        return self._itens

    @itens.setter
    def itens(self, itens: list[ItemFatura]) -> None:
        self._itens = itens

    def adicionar_item(self, item: ItemFatura) -> None:
        """Adiciona um item consumido à fatura."""
        self._itens.append(item)

    def calcular_total(self) -> float:
        """Calcula o valor total de itens consumidos."""
        total = 0.0
        for item in self._itens:
            total += item.item.preco * item.quantidade
        return total

    # Compatibilidade
    add_itens = adicionar_item
    add_item = adicionar_item
    calculate_total = calcular_total


