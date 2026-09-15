from .room_state import State_context
class Quarto:
    TIPOS = ["Simples", "Duplo", "Suíte"]

    def __init__(self, numero: int, tipo: str, valor_diaria: float):
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo inválido. Escolha entre: {self.TIPOS}")
        self._numero = numero
        self._tipo = tipo
        self._valor_diaria = valor_diaria
        self.estado = State_context()

    def get_numero(self) -> int:
        return self._numero

    def get_tipo(self) -> str:
        return self._tipo

    def get_valor_diaria(self) -> float:
        return self._valor_diaria

    def __str__(self):
        status = f" {self.estado.get_current()}"
        return f"Quarto {self._numero} | {self._tipo} | R$ {self._valor_diaria:.2f} | {status}"