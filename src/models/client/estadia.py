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


class Builder(ABC):
    '''Builder abstrato'''
    @property
    @abstractmethod
    def build(self) -> Estadia:
        ...
    @abstractmethod
    def basic_info(self, hospede) -> Any:
        ...
    @abstractmethod
    def checkin(self, data) -> Any:
        ...
    @abstractmethod
    def checkout(self, data) -> Any:
        ...

class Reserva(Builder):
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
    
    def basic_info(self, hospede):
        self.__hospede: Cliente = hospede
        self.__Estado_estadia = Estado_Contexto()
        return self

    def checkin(self, data: date):
        self.__data_prevista_checkin = data # data prevista para o cliente chegar
        return self

    def checkout(self, data: date):
        self.__data_prevista_checkout = data # data prevista para o cliente sair
        return self

class Hospedagem(Builder):
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
    
    def basic_info(self, hospede):
        self.__hospede: Cliente = hospede
        self.__Estado_estadia = Estado_Contexto()
        return self

    def checkin(self, data: date):
        self.__data_checkin = data # data real do checkin
        return self
        
    def checkout(self, data: date):
        self.__data_checkout = data # data real checkout
        return self

class Estadia():
    def __init__(self) -> None:
            self.parts = []

    def list_Dados(self) -> None:
        print(f"Dados: {', '.join(self.parts)}", end=".")


@dataclass
class reserva:
    _id: int| None = None

    
""" 

# https://www.freecodecamp.org/news/how-to-use-the-builder-pattern-in-python-a-practical-guide-for-devs/

class Estadia():
    '''Classe para salvar a estadia do Cliente no Hotel'''
    def __init__(self, hospede: Cliente, quarto: Quarto,
                 consumos: list[Produto], data_prevista_checkin: date, data_prevista_checkout: date, data_entrada: datetime, data_saida: datetime) -> None:
        
        self._id: int | None = None
        self.__hospede: Cliente = hospede
        self.__quarto: Quarto = quarto
        self.__consumos: list[Produto] = consumos
        self.__Estado_estadia = Estado_Contexto()
        self.__data_prevista_checkin = data_prevista_checkin # data prevista para o cliente chegar
        self.__data_prevista_checkout = data_prevista_checkout # data prevista para o cliente sair
        self.__data_entrada = data_entrada # datetime do checkin efetivo
        self.__data_saida = data_saida # datetime do chekout efetivo

    @property
    def get_id(self) -> int | None:
        return self._id
    
    @property
    def get_estado(self) -> str:
        return self.__Estado_estadia.get_nome()

    @property
    def get_hospede(self) -> Cliente:
        return self.__hospede

    @property
    def get_quarto(self) -> Quarto:
        return self.__quarto

    @property
    def get_consumos(self) -> list[Produto]:
        return self.__consumos

    @property
    def get_data_prevista_checkin(self) -> date :
        return self.__data_prevista_checkin

    @property
    def get_data_prevista_checkout(self) -> date :
        return self.__data_prevista_checkout

    @property
    def get_data_entrada(self) -> datetime:
        return self.__data_entrada

    @property
    def get_data_saida(self) -> datetime:
        return self.__data_saida
    
    @get_id.setter
    def id(self, new_id: int) -> None:
        self._id = new_id

    @get_hospede.setter
    def hospede(self, hospede) -> None:
        self.__hospede = hospede

    @get_quarto.setter
    def quarto(self, quarto) -> None:
        self.__quarto = quarto

    @get_consumos.setter
    def consumos(self, consumo) -> None:
        self.__consumos = __consumos

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
        self.__data_saida = now """