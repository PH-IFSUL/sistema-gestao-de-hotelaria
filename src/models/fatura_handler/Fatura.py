

from models.fatura_handler.Produto import Produto


class Fatura():
    def __init__(self, cod: int, estadia, produto, quantidade: int) -> None:
        self._id: int = cod
        self.__estadia = estadia
        self.__produto: list[Produto] = produto
        self.__quantidade: int = quantidade

    @property
    def get_id(self) -> int:
        return self._id
    @get_id.setter
    def set_id(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("id deve ser numero")
        if valor is None:
            raise ValueError("id não pode ser vazio")
        self._id = valor
    @property
    def get_estadia(self):
        return self.__estadia
    @get_estadia.setter
    def set_estadia(self, estadia) -> None:
        self.__estadia = estadia
    @property
    def produto(self):
        return self.__produto
    @produto.setter
    def set_produto(self, produto) -> None:
        self.__produto = produto
    @property
    def get_quantidade(self) -> int:
        return self.__quantidade
    
    @get_quantidade.setter
    def set_quantidade(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("quantidade deve ser numero")
        if valor is None:
            raise ValueError("quantidade não pode ser vazio")
        self.__quantidade = valor
    