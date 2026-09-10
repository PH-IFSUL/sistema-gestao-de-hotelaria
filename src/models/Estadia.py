# imports externos:
from datetime import datetime, date
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# imports locais:
from Estado_estadia import Estado_Contexto
from src.models.Info_datas import Info_data
from src.models.Quarto import Quarto
from src.models.Hospede import Hospede
from src.models.Consumos import Consumos


class Estadia():
    def __init__(self, cod: int, hospede: Hospede, quarto: Quarto,
                 consumos: list[Consumos], estado: Estado_Contexto, info_data: Info_data) -> None:
        
        self._id: int = cod
        self.__hospede: Hospede = hospede
        self.__quarto: Quarto = quarto
        self.__consumos: list[Consumos] = consumos
        self.__info_datas: Info_data = Info_data()
        self.__Estado_estadia = Estado_Contexto()

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("id deve ser numero")
        if valor is None:
            raise ValueError("id não pode ser vazio")
        self._id = valor

    @property
    def hospede(self):
        return self.__hospede

    @hospede.setter
    def hospede(self, hospede) -> None:
        self.__hospede = hospede

    @property
    def quarto(self):
        return self.__quarto

    @quarto.setter
    def quarto(self, quarto) -> None:
        self.__quarto = quarto

    @property
    def consumos(self):
        return self.__consumos

    @consumos.setter
    def consumos(self, consumos) -> None:
        self.__consumos = consumos

    @property
    def info_datas(self):
        return self.__info_datas

    @info_datas.setter
    def info_datas(self, info_datas) -> None:
        self.__info_datas = info_datas
