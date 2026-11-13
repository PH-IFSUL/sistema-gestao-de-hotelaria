"""
Classes para salvar os itens do hotel e os itens da fatura.
"""


class Item:
    """
    Classe para salvar os itens de consumo/serviço do hotel.

    Args:
        id: id do item
        nome: nome do item
        preco: preço do item

    Returns:
        Objeto do tipo Item.
    """

    def __init__(self, id: int, nome: str, preco: float) -> None:
        self._id: int = id
        self._nome: str = nome
        self._preco: float = preco

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id deve ser número")
        if value is None:
            raise ValueError("id não pode ser vazio")
        self._id = value

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("nome deve ser string")
        if value is None:
            raise ValueError("nome não pode ser vazio")
        self._nome = value

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("preço deve ser número")
        if value is None:
            raise ValueError("preço não pode ser vazio")
        self._preco = float(value)

    def __str__(self) -> str:
        return f"Item: {self._nome} - Preço: R${self._preco:.2f}"


class ItemFatura:
    """
    Classe para representar os itens consumidos na fatura da estadia.

    Args:
        id: id do registro do item
        item: objeto do tipo Item
        quantidade: quantidade consumida

    Returns:
        Objeto do tipo ItemFatura.
    """

    def __init__(self, id: int, item: Item, quantidade: int) -> None:
        self._id: int = id
        self._item: Item = item
        self._quantidade: int = quantidade

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id deve ser número")
        if value is None:
            raise ValueError("id não pode ser vazio")
        self._id = value

    @property
    def item(self) -> Item:
        return self._item

    @item.setter
    def item(self, value: Item) -> None:
        if not isinstance(value, Item):
            raise TypeError("item deve ser do tipo Item")
        if value is None:
            raise ValueError("item não pode ser vazio")
        self._item = value

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("quantidade deve ser número inteiro")
        if value is None:
            raise ValueError("quantidade não pode ser vazia")
        self._quantidade = value

