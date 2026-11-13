"""
Classe que serve de interface para a troca dos estados do quarto.
Usando padrão State.
"""
from abc import ABC, abstractmethod


class EstadoContexto:
    """
    Classe que serve de contexto para o gerenciamento dos estados do quarto.
    """

    def __init__(self) -> None:
        self._state: Estado = Disponivel()  # estado inicial do quarto

    def set_estado(self, novo_estado: "Estado") -> None:
        """Define o novo estado do quarto."""
        self._state = novo_estado

    def reservar(self, quarto) -> None:
        self._state.reservar(quarto)

    def check_in(self, quarto) -> None:
        self._state.check_in(quarto)

    def check_out(self, quarto) -> None:
        self._state.check_out(quarto)

    def iniciar_manutencao(self, quarto) -> None:
        self._state.iniciar_manutencao(quarto)

    def finalizar_manutencao(self, quarto) -> None:
        self._state.finalizar_manutencao(quarto)

    def finalizar_limpeza(self, quarto) -> None:
        self._state.finalizar_limpeza(quarto)

    def obter_atual(self) -> str:
        return self._state.obter_atual()

    def __str__(self) -> str:
        return self._state.__str__()

    # Métodos para compatibilidade
    book = reservar
    start_maintenance = iniciar_manutencao
    end_maintenance = finalizar_manutencao
    finish_cleaning = finalizar_limpeza
    get_current = obter_atual


class Estado(ABC):
    """
    Classe base abstrata para os estados do quarto.
    """

    @abstractmethod
    def reservar(self, quarto) -> None:
        ...

    @abstractmethod
    def check_in(self, quarto) -> None:
        ...

    @abstractmethod
    def check_out(self, quarto) -> None:
        ...

    @abstractmethod
    def iniciar_manutencao(self, quarto) -> None:
        ...

    @abstractmethod
    def finalizar_manutencao(self, quarto) -> None:
        ...

    @abstractmethod
    def finalizar_limpeza(self, quarto) -> None:
        ...

    @abstractmethod
    def obter_atual(self) -> str:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    # Métodos para compatibilidade
    def book(self, room) -> None:
        self.reservar(room)

    def start_maintenance(self, room) -> None:
        self.iniciar_manutencao(room)

    def end_maintenance(self, room) -> None:
        self.finalizar_manutencao(room)

    def finish_cleaning(self, room) -> None:
        self.finalizar_limpeza(room)

    def get_current(self) -> str:
        return self.obter_atual()


# Classes concretas dos estados


class Disponivel(Estado):
    """Classe que representa o estado Disponível do quarto."""

    def reservar(self, quarto) -> None:
        quarto.estado.set_estado(Reservado())

    def check_in(self, quarto) -> None:
        quarto.estado.set_estado(Ocupado())

    def check_out(self, quarto) -> None:
        raise TypeError("Quarto Desocupado")

    def iniciar_manutencao(self, quarto) -> None:
        quarto.estado.set_estado(Manutencao())

    def finalizar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto Não está em Manutenção")

    def finalizar_limpeza(self, quarto) -> None:
        raise TypeError("Quarto já está Limpo")

    def obter_atual(self) -> str:
        return "Disponível"

    def __str__(self) -> str:
        return "disponivel"


class Reservado(Estado):
    """Classe que representa o estado Reservado do quarto."""

    def reservar(self, quarto) -> None:
        raise TypeError("Quarto já está reservado")

    def check_in(self, quarto) -> None:
        quarto.estado.set_estado(Ocupado())

    def check_out(self, quarto) -> None:
        raise TypeError("Quarto está Reservado")

    def iniciar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto está Reservado, troque o hóspede de quarto")

    def finalizar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto está Reservado")

    def finalizar_limpeza(self, quarto) -> None:
        raise TypeError("Quarto está Reservado")

    def obter_atual(self) -> str:
        return "Reservado"

    def __str__(self) -> str:
        return "reservado"


class Ocupado(Estado):
    """Classe que representa o estado Ocupado do quarto."""

    def reservar(self, quarto) -> None:
        raise TypeError("Quarto está Ocupado")

    def check_in(self, quarto) -> None:
        raise TypeError("Quarto está Ocupado")

    def check_out(self, quarto) -> None:
        quarto.estado.set_estado(Limpeza())

    def iniciar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto está Ocupado")

    def finalizar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto está Ocupado")

    def finalizar_limpeza(self, quarto) -> None:
        raise TypeError("Quarto está Ocupado")

    def obter_atual(self) -> str:
        return "Ocupado"

    def __str__(self) -> str:
        return "ocupado"


class Limpeza(Estado):
    """Classe que representa o estado Em Limpeza do quarto."""

    def reservar(self, quarto) -> None:
        raise TypeError("Quarto está em Limpeza")

    def check_in(self, quarto) -> None:
        raise TypeError("Quarto está em Limpeza")

    def check_out(self, quarto) -> None:
        raise TypeError("Quarto está em Limpeza")

    def iniciar_manutencao(self, quarto) -> None:
        quarto.estado.set_estado(Manutencao())

    def finalizar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto não está em Manutenção")

    def finalizar_limpeza(self, quarto) -> None:
        quarto.estado.set_estado(Disponivel())

    def obter_atual(self) -> str:
        return "Em Limpeza"

    def __str__(self) -> str:
        return "limpeza"


class Manutencao(Estado):
    """Classe que representa o estado Em Manutenção do quarto."""

    def reservar(self, quarto) -> None:
        raise TypeError("Quarto está em Manutenção")

    def check_in(self, quarto) -> None:
        raise TypeError("Quarto está em Manutenção")

    def check_out(self, quarto) -> None:
        raise TypeError("Quarto está em Manutenção")

    def iniciar_manutencao(self, quarto) -> None:
        raise TypeError("Quarto está em Manutenção")

    def finalizar_manutencao(self, quarto) -> None:
        quarto.estado.set_estado(Limpeza())

    def finalizar_limpeza(self, quarto) -> None:
        raise TypeError("Quarto está em Manutenção")

    def obter_atual(self) -> str:
        return "Em Manutenção"

    def __str__(self) -> str:
        return "manutencao"
