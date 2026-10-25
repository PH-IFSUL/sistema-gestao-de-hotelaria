from models.cliente import Cliente
from models.database.interfaces.cliente_repositorio_interface import ClienteRepositorio


class ClienteController:
    """
    Classe para gerenciar os clientes.

    Args:
        repositorio: repositório de clientes

    Returns:
        Objeto do tipo ClienteController.
    """

    def __init__(self, repositorio: ClienteRepositorio) -> None:
        self._repo = repositorio

    def cadastrar(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str
    ) -> str:
        nome = nome.strip()
        cpf = cpf.strip()
        telefone = telefone.strip()
        email = email.strip()

        if not nome:
            raise ValueError("O campo Nome é obrigatório.")
        if not cpf:
            raise ValueError("O campo CPF é obrigatório.")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        if not telefone:
            raise ValueError("O campo Telefone é obrigatório.")

        cliente = Cliente(nome, cpf, telefone, email)
        self._repo.salvar(cliente)
        return f"Cliente '{nome}' cadastrado com sucesso."

    def listar(self) -> list[Cliente]:
        return self._repo.obter_todos()

    def remover(self, cpf: str) -> str:
        cpf = cpf.strip()
        if not self._repo.remover(cpf):
            raise ValueError(f"Nenhum cliente encontrado com CPF {cpf}.")
        return f"Cliente com CPF {cpf} removido."

