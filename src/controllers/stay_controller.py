from datetime import date, datetime
from models.room.room import Room
from models.client.client import Client
from models.client.stay_info import Guest_Stay, Reservation
from models.database.interfaces.client_repository_interface import Client_Repository
from models.database.interfaces.room_repository_interface import Room_Repository


class Stay_Controller:
    def __init__(self, room_repo: Room_Repository, client_repo: Client_Repository):
        self._room_repo = room_repo
        self._client_repo = client_repo

    def make_reservation(self, client: Client, room: Room, start_date: date, end_date: date):
        pass

    def add_client_to_stay(self, stay: Guest_Stay, client: Client):
        pass

    def add_room_to_stay(self, stay: Guest_Stay, room: Room):
        pass

    def remove_client_from_stay(self, stay: Guest_Stay, client: Client):
        pass

    def remove_room_from_stay(self, stay: Guest_Stay, room: Room):
        pass
    
    def check_in(self, stay: Guest_Stay, check_in_date: datetime):
        pass

    def check_out(self, stay: Guest_Stay, check_out_date: datetime):
        pass

    def get_all_stays(self):
        pass

    def get_all_reservations(self):
        pass
