
class Hospede:
    def __init__(self, cod: int, nome: str, idade: int, cpf: str, telefone: str, email: str) -> None:
        self.__id = cod
        self.__nome = nome
        self.__idade = idade
        self.__cpf = cpf
        self.__telefone = telefone
        self.__email = email

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
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser string")
        if nome is None:
            raise ValueError("nome não pode ser vazio")
        self.__nome = nome
    
    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, idade: int):
        if not isinstance(idade, int):
            raise TypeError("idade deve ser um número")
        if idade is None:
            raise ValueError("idade não pode ser vazio")
        self.__idade = idade

    @property
    def cpf(self) -> str:
        return self.__cpf
    
    @cpf.setter
    def cpf(self, cpf: str):
        if not isinstance(cpf, str):
            raise TypeError("cpf deve ser uma string")
        if cpf is None:
            raise ValueError("cpf não pode ser vazio")
        self.__cpf = cpf

    @property
    def telefone(self) -> str:
        return self.__telefone
    @telefone.setter
    def telefone(self, telefone: str):
        if not isinstance(telefone, str):
            raise TypeError("telefone deve ser uma string")
        if telefone is None:
            raise ValueError("telefone não pode ser vazio")
        self.__telefone = telefone

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        if not isinstance(email, str):
            raise TypeError("email deve ser uma string")
        if email is None:
            raise ValueError("email não pode ser vazio")
        self.__email = email

    def cadastrar_hospede(self, id: int, nome: str, idade: int, cpf: str, telefone: str, email: str):
        self.id = id
        self.__nome = nome
        self.__idade = idade
        self.__cpf = cpf
        self.__telefone = telefone
        self.__email = email

    def editar_hospede(self, nome: str = None, idade: int = None, cpf: str = None, telefone: str = None, email: str = None):
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
        if isinstance(other, Hospede):
            return self.id == other.id
        return False

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.__nome}, Idade: {self.__idade}, CPF: {self.__cpf}, Telefone: {self.__telefone}, Email: {self.__email}"