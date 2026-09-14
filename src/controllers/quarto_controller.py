from models.room.quarto import Quarto
from models.database.interfaces.room_repository_interface import RoomRepository

class QuartoController:
    def __init__(self, repositorio: RoomRepository):
        self._repo = repositorio

    def cadastrar(self, 
                  numero_str: str,
                  tipo: str,
                  valor_str: str) -> str:
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
            raise ValueError("Valor da diária deve ser um número "
                             "(ex: 150.00).")

        if valor <= 0:
            raise ValueError("Valor da diária deve ser maior que zero.")

        quarto = Quarto(int(numero_str), tipo, valor)
        self._repo.add(quarto)
        return f"Quarto {numero_str} ({tipo}) cadastrado com sucesso."

    def listar(self) -> list[Quarto]:
        return self._repo.list()

    def remover(self, numero_str: str) -> str:
        numero_str = numero_str.strip()
        if not numero_str.isdigit():
            raise ValueError("Informe um número de quarto válido.")
        if not self._repo.delete(int(numero_str)):
            raise ValueError(f"Nenhum quarto encontrado com número "
                             f" {numero_str}.")
        return f"Quarto {numero_str} removido."
