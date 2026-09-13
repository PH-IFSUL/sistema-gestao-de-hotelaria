from .Quarto import Quarto

class QuartoRepositorio:
    def __init__(self):
        self._quartos: list[Quarto] = []

    def adicionar(self, quarto: Quarto) -> None:
        if self.buscar_por_numero(quarto.get_numero()):
            raise ValueError(f"Já existe um quarto com o número {quarto.get_numero()}.")
        self._quartos.append(quarto)

    def listar(self) -> list[Quarto]:
        return list(self._quartos)

    def buscar_por_numero(self, numero: int) -> Quarto | None:
        for q in self._quartos:
            if q.get_numero() == numero:
                return q
        return None

    def remover(self, numero: int) -> bool:
        quarto = self.buscar_por_numero(numero)
        if quarto:
            self._quartos.remove(quarto)
            return True
        return False
