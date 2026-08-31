from datetime import datetime, date
from Estado_estadia import Estado_Contexto


class Estadia():
    def __init__(self, cod: int, hospede, quarto,
                 data_chekin_prevista: date, 
                 data_chekout_prevista: date) -> None:
        
        self._id: int = cod
        self.__hospede: None = hospede
        self.__quarto: None = quarto
        self.__Estado_estadia = Estado_Contexto()
        self.__data_chekin_prevista: date = data_chekin_prevista
        self.__data_chekout_prevista: date = data_chekout_prevista
        self.__data_checkin: None | datetime = None
        self.__data_chekout: None | datetime = None

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
