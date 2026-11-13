from .estado_quarto import EstadoContexto


class Quarto:
    """
    Classe para representar os quartos do hotel.

    Args:
        numero: número do quarto
        tipo: tipo do quarto (Simples, Duplo, Suíte)
        valor_diaria: valor da diária do quarto

    Returns:
        Objeto do tipo Quarto.
    """

    TIPOS = ["Simples", "Duplo", "Suíte"]

    def __init__(self, numero: int, tipo: str, valor_diaria: float) -> None:
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo inválido. Escolha entre: {self.TIPOS}")
        self._numero = numero
        self._tipo = tipo
        self._valor_diaria = valor_diaria
        self.estado = EstadoContexto()

    def get_numero(self) -> int:
        return self._numero

    def get_tipo(self) -> str:
        return self._tipo

    def get_valor_diaria(self) -> float:
        return self._valor_diaria

    def __str__(self) -> str:
        status = f" {self.estado.obter_atual()}"
        return f"Quarto {self._numero} | {self._tipo} | R$ {self._valor_diaria:.2f} | {status}"


