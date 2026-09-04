from abc import ABC, abstractmethod
import datetime

class Estado_Contexto:
    '''
    classe que serve de interface entre os estados da estadia do
    Hospede.
    '''
    def __init__(self) -> None:
        self._state = Reservada()  # estado inicial da estadia

    def set_estado(self, novo_estado):
        # usado para definir novo estado
        self._state = novo_estado

    def get_nome(self):
        return self._state.get_nome()

    def finalizar(self):
        self._state.finalizar(self)


class State(ABC):
    @abstractmethod
    def iniciar(self, estadia):
        pass
    @abstractmethod
    def finalizar(self, estadia):
        pass
    @abstractmethod
    def get_nome(self) -> str:
        pass


#classes concretas dos estados

class Reservada(State):
    def iniciar(self, estadia):
        estadia.__Estado_estadia.set_estado(Reservada())
        estadia.info_datas.reservar(estadia.info_datas.data_checkin_previsto, estadia.info_datas.data_checkout_previsto)
        estadia.info_datas.data_atualizado = datetime.datetime.now()
        
    def finalizar(self, estadia):
        pass

    def get_nome(self):
        return "Reservada"
    
class Em_estadia(State):
    def iniciar(self, estadia):
        pass

    def get_nome(self):
        return "Em Estadia"
    
class Chekout_realizado(State):
    def iniciar(self, estadia):
        pass

    def get_nome(self):
        return "Checkout Realizado"
    