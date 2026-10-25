from datetime import datetime, date
from .quarto import Quarto
from .cliente import Cliente
from .fatura import Fatura
from .item import ItemFatura


class Reserva:
    """
    Classe para salvar a reserva do cliente.

    Args:
        hospede: Objeto do cliente/hóspede.
        data_checkin: Data prevista para o check-in.
        data_checkout: Data prevista para o check-out.

    Returns:
        Objeto do tipo Reserva.
    """

    def __init__(
        self,
        hospede: Cliente,
        data_checkin: date,
        data_checkout: date
    ) -> None:
        self._id: int | None = None
        self._hospede: Cliente = hospede
        self._data_checkin: date = data_checkin
        self._data_checkout: date = data_checkout

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        self._id = valor

    @property
    def hospede(self) -> Cliente:
        return self._hospede

    @hospede.setter
    def hospede(self, hospede: Cliente) -> None:
        self._hospede = hospede

    @property
    def data_checkin(self) -> date:
        return self._data_checkin

    @data_checkin.setter
    def data_checkin(self, valor: date) -> None:
        self._data_checkin = valor

    @property
    def data_checkout(self) -> date:
        return self._data_checkout

    @data_checkout.setter
    def data_checkout(self, valor: date) -> None:
        self._data_checkout = valor

    # Compatibilidade
    @property
    def guest(self) -> Cliente:
        return self._hospede

    @guest.setter
    def guest(self, hospede: Cliente) -> None:
        self._hospede = hospede

    @property
    def checkin_date(self) -> date:
        return self._data_checkin

    @checkin_date.setter
    def checkin_date(self, valor: date) -> None:
        self._data_checkin = valor

    @property
    def checkout(self) -> date:
        return self._data_checkout

    @checkout.setter
    def checkout(self, valor: date) -> None:
        self._data_checkout = valor


class Estadia:
    """
    Classe para representar a estadia do cliente no hotel.

    Args:
        hospede: Objeto do tipo Cliente.
        quarto: Objeto do tipo Quarto alocado (ou None).
        data_checkin: Data/hora do check-in.
        data_checkout: Data/hora do check-out.

    Returns:
        Objeto do tipo Estadia.
    """

    def __init__(
        self,
        hospede: Cliente,
        quarto: Quarto | None,
        data_checkin: datetime,
        data_checkout: datetime
    ) -> None:
        self._id: int | None = None
        self._hospede: Cliente = hospede
        self._quarto: Quarto | None = quarto
        self._data_checkin: datetime = data_checkin
        self._data_checkout: datetime = data_checkout
        self._fatura: Fatura = Fatura()

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, novo_id: int) -> None:
        self._id = novo_id

    @property
    def hospede(self) -> Cliente:
        return self._hospede

    @hospede.setter
    def hospede(self, hospede: Cliente) -> None:
        self._hospede = hospede

    @property
    def quarto(self) -> Quarto | None:
        return self._quarto

    @quarto.setter
    def quarto(self, quarto: Quarto | None) -> None:
        self._quarto = quarto

    @property
    def fatura(self) -> Fatura:
        return self._fatura

    @fatura.setter
    def fatura(self, fatura: Fatura) -> None:
        self._fatura = fatura

    @property
    def data_checkin(self) -> datetime:
        return self._data_checkin

    @property
    def data_checkout(self) -> datetime:
        return self._data_checkout

    def obter_total(self) -> float:
        return self._fatura.calcular_total()

    def adicionar_item(self, item: ItemFatura) -> None:
        self._fatura.adicionar_item(item)

    # Compatibilidade
    @property
    def guest(self) -> Cliente:
        return self._hospede

    @guest.setter
    def guest(self, hospede: Cliente) -> None:
        self._hospede = hospede

    @property
    def room_number(self) -> Quarto | None:
        return self._quarto

    @room_number.setter
    def room_number(self, quarto: Quarto | None) -> None:
        self._quarto = quarto

    @property
    def guest_bill(self) -> Fatura:
        return self._fatura

    @guest_bill.setter
    def guest_bill(self, fatura: Fatura) -> None:
        self._fatura = fatura

    @property
    def checkin_date(self) -> datetime:
        return self._data_checkin

    @property
    def checkout_date(self) -> datetime:
        return self._data_checkout

