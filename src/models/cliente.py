class Cliente:
    """
    Classe para gerenciar os dados dos clientes.

    Args:
        nome: nome do cliente
        cpf: cpf do cliente
        telefone: telefone do cliente
        email: email do cliente
        id: id do cliente (opcional)

    Returns:
        Objeto do tipo Cliente.
    """

    def __init__(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
        id: int | None = None
    ) -> None:
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cliente):
            return self._id == other._id
        return False


