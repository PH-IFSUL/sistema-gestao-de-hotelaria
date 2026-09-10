import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.models.model import Cliente, Quarto, ClienteRepositorio, QuartoRepositorio


class ClienteController:
    def __init__(self, repositorio: ClienteRepositorio):
        self._repo = repositorio

    def cadastrar(self, nome: str, cpf: str, telefone: str, email: str) -> str:
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
        self._repo.adicionar(cliente)
        return f"Cliente '{nome}' cadastrado com sucesso."

    def listar(self) -> list[Cliente]:
        return self._repo.listar()

    def remover(self, cpf: str) -> str:
        cpf = cpf.strip()
        if not self._repo.remover(cpf):
            raise ValueError(f"Nenhum cliente encontrado com CPF {cpf}.")
        return f"Cliente com CPF {cpf} removido."


class QuartoController:
    def __init__(self, repositorio: QuartoRepositorio):
        self._repo = repositorio

    def cadastrar(self, numero_str: str, tipo: str, valor_str: str) -> str:
        numero_str = numero_str.strip()
        valor_str = valor_str.strip().replace(",", ".")

        if not numero_str:
            raise ValueError("O campo Número é obrigatório.")
        if not numero_str.isdigit():
            raise ValueError("Número do quarto deve ser um valor inteiro.")
        if not tipo:
            raise ValueError("Selecione um tipo de quarto.")
        if not valor_str:
            raise ValueError("O campo Valor da Diária é obrigatório.")

        try:
            valor = float(valor_str)
        except ValueError:
            raise ValueError("Valor da diária deve ser um número (ex: 150.00).")

        if valor <= 0:
            raise ValueError("Valor da diária deve ser maior que zero.")

        quarto = Quarto(int(numero_str), tipo, valor)
        self._repo.adicionar(quarto)
        return f"Quarto {numero_str} ({tipo}) cadastrado com sucesso."

    def listar(self) -> list[Quarto]:
        return self._repo.listar()

    def remover(self, numero_str: str) -> str:
        numero_str = numero_str.strip()
        if not numero_str.isdigit():
            raise ValueError("Informe um número de quarto válido.")
        if not self._repo.remover(int(numero_str)):
            raise ValueError(f"Nenhum quarto encontrado com número {numero_str}.")
        return f"Quarto {numero_str} removido."
