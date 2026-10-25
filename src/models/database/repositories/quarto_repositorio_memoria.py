from typing import List, Optional
from ...quarto import Quarto


class QuartoRepositorioMemoria:
    """
    Implementação em memória da interface QuartoRepositorio.
    """

    def __init__(self) -> None:
        self._quartos: List[Quarto] = []

    def adicionar(self, quarto: Quarto) -> None:
        if self.buscar_por_numero(quarto.get_numero()):
            raise ValueError(f"Já existe um quarto com o número {quarto.get_numero()}.")
        self._quartos.append(quarto)

    def listar(self) -> List[Quarto]:
        return list(self._quartos)

    def buscar_por_numero(self, numero_busca: int) -> Optional[Quarto]:
        for q in self._quartos:
            if q.get_numero() == numero_busca:
                return q
        return None

    def remover(self, numero_busca: int) -> bool:
        quarto = self.buscar_por_numero(numero_busca)
        if quarto:
            self._quartos.remove(quarto)
            return True
        return False

    def obter_tipos(self) -> List[str]:
        tipos = []
        for quarto in self._quartos:
            if quarto.get_tipo() not in tipos:
                tipos.append(quarto.get_tipo())
        return tipos

