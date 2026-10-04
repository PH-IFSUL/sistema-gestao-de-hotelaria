from .itens import Bill_Item

class Guest_Bill():
    """Classe para salvar a fatura do cliente
    
    Args:
        id_stay: id da estadia
    
    Returns:
        Objeto do tipo Guest_Bill.
    """
    def __init__(self, id_stay: int) -> None:
        self._id_stay: int = id_stay
        self.__itens: list[Bill_Item] = list()

    @property
    def id_stay(self) -> int:
        return self._id_stay
    @id_stay.setter
    def id_stay(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("id deve ser numero")
        if value is None:
            raise ValueError("id não pode ser vazio")
        self._id_stay = value

    @property
    def itens(self):
        return self.__itens
    @itens.setter
    def set_itens(self, itens) -> None:
        self.__itens = itens

    def add_itens(self, item: Bill_Item) -> None:
        self.__itens.append(item)

    def calculate_total(self) -> float:
        total = 0.0
        for item in self.__itens:
            total += item.price * item.quantity
        return total