

class Consumos():
    def __init__(self, cod: int, estadia, produto, quantidade: int) -> None:
        self._id: int = cod
        self.__estadia = estadia
        self.__produto: list[Produto] = produto
        self.__quantidade: int = quantidade

    @property
    def id(self) -> int:
        return self._id
    @id.setter
    def id(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("id deve ser numero")
        if valor is None:
            raise ValueError("id não pode ser vazio")
        self._id = valor
    @property
    def estadia(self):
        return self.__estadia
    @estadia.setter
    def estadia(self, estadia) -> None:
        self.__estadia = estadia
    @property
    def produto(self):
        return self.__produto
    @produto.setter
    def produto(self, produto) -> None:
        self.__produto = produto
    @property
    def quantidade(self) -> int:
        return self.__quantidade
    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("quantidade deve ser numero")
        if valor is None:
            raise ValueError("quantidade não pode ser vazio")
        self.__quantidade = valor
    