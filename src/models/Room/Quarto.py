from .Tipos_quarto import TiposQuarto

class Quarto:

    def __init__(self, numero: int, tipo: str, valor_diaria: float):
        if tipo not in TiposQuarto:
            raise ValueError(f"Tipo inválido. Escolha entre: {list(TiposQuarto)}")
        self._numero = numero
        self._tipo = tipo
        self._valor_diaria = valor_diaria
        self._disponivel = True

    def get_numero(self) -> int:
        return self._numero

    def get_tipo(self) -> str:
        return self._tipo

    def get_valor_diaria(self) -> float:
        return self._valor_diaria

    def is_disponivel(self) -> bool:
        return self._disponivel

    def bloquear(self):
        self._disponivel = False

    def liberar(self):
        self._disponivel = True

    def __str__(self):
        status = "Disponível" if self._disponivel else "Ocupado"
        return f"Quarto {self._numero} | {self._tipo} | R$ {self._valor_diaria:.2f} | {status}"