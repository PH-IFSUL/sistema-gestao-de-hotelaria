class Produto():
    def __init__(self, cod: int, nome: str, preco: float) -> None:
        self._id: int = cod
        self.__nome: str = nome
        self.__preco: float = preco

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
    def get_nome(self) -> str:
        return self.__nome
    @get_nome.setter
    def set_nome(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("nome deve ser string")
        if valor is None:
            raise ValueError("nome não pode ser vazio")
        self.__nome = valor

    @property
    def get_preco(self) -> float:
        return self.__preco
    
    @get_preco.setter
    def set_preco(self, valor: float) -> None:
        if not isinstance(valor, float):
            raise TypeError("preco deve ser numero")
        if valor is None:
            raise ValueError("preco não pode ser vazio")
        self.__preco = valor
