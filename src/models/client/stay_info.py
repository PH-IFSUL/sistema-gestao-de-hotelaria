from datetime import datetime, date
from ..room.room import Room
from ..client.client import Client
from ..invoice.invoice import Guest_Bill
from ..invoice.itens import Bill_Item


class Reservation():
    """Classe para salvar a rederva do cliente
    
        Args:
            guest: Objeto do hospede.
            checkin_date: data prevista para o checkin.
            checkout_date: data prevista para o checkout.
    
        Returns:
            Objeto do tipo reserva.
    """
    def __init__(self, guest: Client, 
                checkin: date, 
                checkout: date) -> None:
        self._id: int | None = None
        self.__guest: Client = guest
        self.__checkin: date = checkin
        self.__checkout: date = checkout

    @property
    def guest(self) -> Client:
        return self.__guest
    @guest.setter
    def guest(self, guest) -> None:
        self.__guest = guest
    @property
    def checkin_date(self) -> date:
        return self.__checkin
    @checkin_date.setter
    def checkin_date(self, date) -> None:
        self.__checkin = date

    @property
    def checkout(self) -> date:
        return self.__checkout
    @checkout.setter
    def checkout(self, date) -> None:
        self.__checkout= date
        
class Guest_Stay():
    """Classe para salvar a estadia do Cliente no Hotel

    Args:
        guest: Objeto do hospede.
        room_number: numero do quarto
        checkin_date: datetime do checkin
        checkout_date: datetime do checkin

    Returns:
        Objeto do tipo Guest_Stay.
    """
    
    def __init__(self, guest: Client, 
                 room_number: Room | None,
                 checkin_date: datetime, 
                 checkout_date: datetime) -> None:
        
        self._id: int | None = None
        self.__guest: Client = guest
        self.__room_number: Room | None = room_number
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date
        self.__guest_bill = Guest_Bill()

    @property
    def id(self) -> int | None:
        return self._id
    @id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id
    
    @property
    def guest(self) -> Client:
        return self.__guest
    @guest.setter
    def guest(self, guest) -> None:
        self.__guest = guest

    @property
    def room_number(self) -> Room | None:
        return self.__room_number
    @room_number.setter
    def room_number(self, room_number: Room | None) -> None:
        self.__room_number = room_number

    @property
    def guest_bill(self) -> Guest_Bill:
        return self.__guest_bill
    @guest_bill.setter
    def guest_bill(self, guest_bill: Guest_Bill) -> None:
        self.__guest_bill = guest_bill

    @property
    def checkin_date(self) -> datetime:
        return self.__checkin_date

    @property
    def checkout_date(self) -> datetime:
        return self.__checkout_date
    
    def get_total(self) -> float:
        return self.__guest_bill.calculate_total()
    
    def add_item(self, item: Bill_Item) -> None:
        self.__guest_bill.add_item(item)