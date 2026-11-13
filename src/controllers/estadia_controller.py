from datetime import date, datetime
from models.quarto import Quarto
from models.cliente import Cliente
from models.estadia import Estadia, Reserva
from models.database.interfaces.cliente_repositorio_interface import ClienteRepositorio
from models.database.interfaces.quarto_repositorio_interface import QuartoRepositorio


class EstadiaController:
    """
    Controlador responsável pelo gerenciamento de estadias e reservas.
    """

    def __init__(
        self,
        cliente_repo: ClienteRepositorio,
        quarto_repo: QuartoRepositorio
    ) -> None:
        self._cliente_repo = cliente_repo
        self._quarto_repo = quarto_repo

    def realizar_reserva(
        self,
        cliente: Cliente,
        quarto: Quarto,
        data_inicio: date,
        data_fim: date
    ):
        pass

    def adicionar_cliente_estadia(self, estadia: Estadia, cliente: Cliente):
        pass

    def adicionar_quarto_estadia(self, estadia: Estadia, quarto: Quarto):
        pass

    def remover_cliente_estadia(self, estadia: Estadia, cliente: Cliente):
        pass

    def remover_quarto_estadia(self, estadia: Estadia, quarto: Quarto):
        pass

    def check_in(self, estadia: Estadia, data_checkin: datetime):
        pass

    def check_out(self, estadia: Estadia, data_checkout: datetime):
        pass

    def obter_todas_estadias(self):
        pass

    def obter_todas_reservas(self):
        pass


