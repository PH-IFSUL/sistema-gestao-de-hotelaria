
class Quarto():
    def __init__(self, cod: int, andar: int, quantidade_camas: int, tipo: str, preco: float) -> None:
        self._id: int = cod
        self.__andar: int = andar
        self.__quantidade_camas: int = quantidade_camas
        self.__tipo: str = tipo
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
    def andar(self) -> int:
        return self.__andar
    @andar.setter
    def andar(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("andar deve ser numero")
        if valor is None:
            raise ValueError("andar não pode ser vazio")
        self.__andar = valor

    @property
    def quantidade_camas(self) -> int:
        return self.__quantidade_camas
    @quantidade_camas.setter
    def quantidade_camas(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("quantidade_camas deve ser numero")
        if valor is None:
            raise ValueError("quantidade_camas não pode ser vazio")
        self.__quantidade_camas = valor

    @property
    def tipo(self) -> str:
        return self.__tipo
    @tipo.setter
    def tipo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("tipo deve ser string")
        if valor is None:
            raise ValueError("tipo não pode ser vazio")
        self.__tipo = valor

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

    def cadastrar_quarto(self, cod: int, andar: int, quantidade_camas: int, tipo: str, preco: float) -> None:
        self._id = cod
        self.__andar = andar
        self.__quantidade_camas = quantidade_camas
        self.__tipo = tipo
        self.__preco = preco
    

    def __str__(self) -> str:
        return f"Quarto {self._id} - Andar: {self.__andar}, Camas: {self.__quantidade_camas}, Tipo: {self.__tipo}, Preço: {self.__preco}"
    