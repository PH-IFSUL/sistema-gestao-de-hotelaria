class Cliente:
    def __init__(self, id: int, nome: str, cpf: str, idade: int, telefone: str, email: str):
        self.__id = id
        self.__nome = nome
        self.__cpf = cpf
        self.__idade = idade
        self.__telefone = telefone
        self.__email = email

    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_cpf(self) -> str:
        return self.__cpf

    def get_idade(self) -> int:
        return self.__idade

    def get_telefone(self) -> str:
        return self.__telefone

    def get_email(self) -> str:
        return self.__email

    def __str__(self):
        return f"{self.__nome} (CPF: {self.__cpf})"

    def editar_cliente(self, nome: str | None = None, idade: int | None = None, cpf: str | None = None, telefone: str | None = None, email: str | None = None):
        if nome is not None:
            self.__nome = nome
        if idade is not None:
            self.__idade = idade
        if cpf is not None:
            self.__cpf = cpf
        if telefone is not None:
            self.__telefone = telefone
        if email is not None:
            self.__email = email

    def __eq__(self, other):
        if isinstance(other, Cliente):
            return self.__id == other.__id
        return False