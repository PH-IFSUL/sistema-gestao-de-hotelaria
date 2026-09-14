
class Cliente:
    def __init__(self, nome: str, cpf: str, telefone: str, email: str):
        self._id: int # gerada quando o cliente é salvo
        self._nome = nome
        self._cpf = cpf
        # self.__idade = idade
        self._telefone = telefone
        self._email = email

    def get_id(self) -> int:
        return self._id

    def get_nome(self) -> str:
        return self._nome

    def get_cpf(self) -> str:
        return self._cpf

    """  def get_idade(self) -> int:
        return self.__idade """

    def get_telefone(self) -> str:
        return self._telefone

    def get_email(self) -> str:
        return self._email

    def __str__(self):
        return f"{self._nome} (CPF: {self._cpf})"

    """ def editar_cliente(self, nome: str | None = None, idade: int | None = None, cpf: str | None = None, telefone: str | None = None, email: str | None = None):
        if nome is not None:
            self._nome = nome
        if idade is not None:
            self.__idade = idade 
        if cpf is not None:
            self._cpf = cpf
        if telefone is not None:
            self._telefone = telefone
        if email is not None:
            self._email = email
    """
    """ def __eq__(self, other):
        if isinstance(other, Cliente):
            return self._id == other._id
        return False """