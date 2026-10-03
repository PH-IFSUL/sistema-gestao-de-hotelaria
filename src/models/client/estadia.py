# imports externos:
from __future__ import annotations
from typing import Any
from datetime import datetime, date
from dataclasses import dataclass
from abc import ABC, abstractmethod
# imports locais:
from .state_estadia import Estado_Contexto
from ..room.room import Quarto
from ..client.cliente import Cliente
from ..product.produto import Produto
# from ..database.interfaces.estadia_interface import get_next_id, EstadiaRepository


class BuilderEstadia(ABC):
    '''Builder abstrato'''
    @property
    @abstractmethod
    def build(self) -> Estadia:
        ...
    @abstractmethod
    def add_cliente(self, hospede: Cliente) -> Any:
        ...

class Reserva(BuilderEstadia):
    '''Builder concreto da reserva'''
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._reserva = Estadia()

    @property
    def build(self):
        reserva = self._reserva
        self.reset()
        return reserva
    
    def add_cliente(self, hospede):
        self._reserva.add(hospede)
        return self

    def checkin(self, data_prevista: date):
        self._reserva.add(data_prevista) # data prevista para o cliente chegar
        return self

    def checkout(self, data_prevista: date):
        self.__data_prevista_checkout = data_prevista # data prevista para o cliente sair
        return self

class Hospedagem(BuilderEstadia):
    '''Builder concreto da hospedagem'''
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._hospedagem = Estadia()

    @property
    def build(self):
        hospedagem = self._hospedagem
        self.reset()
        return hospedagem
    
    def add_cliente(self, hospede: Cliente):
        self._hospedagem._hospede = hospede
        return self

    def checkin(self):
        self.__data_checkin = datetime.now() # data real do checkin
        return self
        
    def checkout(self):
        self.__data_checkout = datetime.now() # data real checkout
        return self


# https://www.freecodecamp.org/news/how-to-use-the-builder-pattern-in-python-a-practical-guide-for-devs/

class Estadia():
    '''Classe para salvar a estadia do Cliente no Hotel'''
    def __init__(self) -> None:
        self._id = None
        self._hospede: Cliente | None = None
        self._quarto = None
        self._consumos: list[Produto] = []
        self._data_prevista_checkin = None # data prevista para o cliente chegar
        self._data_prevista_checkout = None # data prevista para o cliente sair
        self._data_entrada = None # datetime do checkin efetivo
        self._data_saida = None # datetime do chekout efetivo

    @property
    def get_id(self) -> int | None:
        return self._id

    @property
    def hospede(self) -> Cliente | None:
        return self._hospede

    @property
    def get_quarto(self) -> Quarto:
        return self.__quarto

    @property
    def get_consumos(self) -> list[Produto]:
        return self._consumos

    @property
    def get_data_prevista_checkin(self) -> date :
        return self._data_prevista_checkin

    @property
    def get_data_prevista_checkout(self) -> date :
        return self._data_prevista_checkout

    @property
    def get_data_entrada(self) -> datetime:
        return self._data_entrada

    @property
    def get_data_saida(self) -> datetime:
        return self._data_saida
    
    @get_id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @hospede.setter
    def hospede(self, hospede: Cliente) -> None:
        self._hospede = hospede

    @get_quarto.setter
    def quarto(self, quarto) -> None:
        self.__quarto = quarto

    @get_consumos.setter
    def consumos(self, consumo) -> None:
        self._consumos = _consumos

    @get_data_prevista_checkin.setter
    def data_prevista_checkin(self, data: date) ->None:
        self.__data_prevista_checkin = data    
    
    @get_data_prevista_checkout.setter
    def data_prevista_checkout(self, data: date) ->None:
        self.__data_prevista_checkout = data

    @get_data_entrada.setter
    def data_entrada(self, now: datetime) -> None:
        self.__data_entrada = now

    @get_data_saida.setter
    def get_data_saida(self, now: datetime) -> None:
        self.__data_saida = now 