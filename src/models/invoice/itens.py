"""
    Aqui vão ficar as classes para salvar os itens do hotel
    e os itens da fatura
"""

class Item:
    ''' Classe para salvar os itens do hotel
    
        Args:
            id: id do item
            name: nome do item
            price: preço do item
    
        Returns:
            Objeto do tipo Item.
    '''
    def __init__(self, id: int, name: str, price: float) -> None:
        self._id: int = id
        self.__name: str = name
        self.__price: float = price

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id deve ser numero")
        if value is None:
            raise ValueError("id não pode ser vazio")
        self._id = value

    @property
    def name(self) -> str:
        return self.__name
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("nome deve ser string")
        if value is None:
            raise ValueError("nome não pode ser vazio")
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price
    
    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("preco deve ser numero")
        if value is None:
            raise ValueError("preco não pode ser vazio")
        self.__price = value

    def __str__(self) -> str:
        return f"Item: {self.__name} - Preço: R${self.__price}"

class Bill_Item:
    ''' Classe para salvar os itens da fatura
    
        Args:
            id: id do item
            item: item
            quantity: quantidade do item
    
        Returns:
            Objeto do tipo Bill_Item.
    '''
    def __init__(self, id: int, item: Item, quantity: int) -> None:
        self._id: int = id
        self.__item: Item = item
        self.__quantity: int = quantity

    @property
    def item(self) -> Item:
        return self.__item
    @item.setter
    def item(self, value: Item) -> None:
        if not isinstance(value, Item):
            raise TypeError("item deve ser Item")
        if value is None:
            raise ValueError("item não pode ser vazio")
        self.__item = value

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id deve ser numero")
        if value is None:
            raise ValueError("id não pode ser vazio")
        self._id = value

    @property
    def quantity(self) -> int:
        return self.__quantity
    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("quantidade deve ser numero")
        if value is None:
            raise ValueError("quantidade não pode ser vazio")
        self.__quantity = value

    def __str__(self) -> str:
        return f"Item: {self.__item.name} - Preço: R${self.__item.price} - Quantidade: {self.__quantity}"
