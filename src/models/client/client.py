
class Client:
    """
    Classe para gerenciar os dados dos clientes.
    
        Args:
            id: id do cliente
            nome: nome do cliente
            cpf: cpf do cliente
            telefone: telefone do cliente
            email: email do cliente
            birth_date: data de nascimento do cliente
    
        Returns:
            Objeto do tipo Cliente.
    """

    def __init__(self, 
                nome: str, 
                cpf: str, 
                telefone: str, 
                email: str, 
                id: int | None = None) -> None:

        self._id: int | None = id
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone
        self._email = email

    def get_id(self) -> int | None:
        return self._id

    def set_id(self, id: int) -> None:
        self._id = id

    def get_nome(self) -> str:
        return self._nome

    def get_cpf(self) -> str:
        return self._cpf

    def get_telefone(self) -> str:
        return self._telefone

    def get_email(self) -> str:
        return self._email

    def __str__(self) -> str:
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Client):
            return self._id == other._id
        return False