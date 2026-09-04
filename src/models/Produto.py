

class Produto():
    def __init__(self, cod: int, nome: str, preco: float) -> None:
        self._id: int = cod
        self.__nome: str = nome
        self.__preco: float = preco

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
    def nome(self) -> str:
        return self.__nome
    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("nome deve ser string")
        if valor is None:
            raise ValueError("nome não pode ser vazio")
        self.__nome = valor

    @property
    def preco(self) -> float:
        return self.__preco
    @preco.setter
    def preco(self, valor: float) -> None:
        if not isinstance(valor, float):
            raise TypeError("preco deve ser numero")
        if valor is None:
            raise ValueError("preco não pode ser vazio")
        self.__preco = valor
