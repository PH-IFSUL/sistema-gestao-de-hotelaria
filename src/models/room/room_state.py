
from abc import ABC, abstractmethod

class State_context:
    '''
    classe que serve de interface para a troca dos estados do quarto.
    '''
    def __init__(self) -> None:
        self._state = Available()  # estado inicial do quarto

    def set_estado(self, new_state) -> None: # usado para definir novo estado
        self._state = new_state

    def book(self, room) -> None: # reservar
        self._state.book(room)

    def check_in(self, room) -> None:
        self._state.check_in(room)

    def check_out(self, room) -> None:
        self._state.check_out(room)

    def start_maintenance(self, room) -> None:
        self._state.start_maintenance(room)

    def end_maintenance(self, room) -> None:
        self._state.end_maintenance(room)

    def finish_cleaning(self, room) -> None:
            self._state.finish_cleaning(room)

    def get_current(self) -> str:
        return self._state.get_current()
    
    def __str__(self) -> str:
        return self._state.__str__()

class State(ABC):
    @abstractmethod
    def book(self, room) -> None:
        ...
    @abstractmethod
    def check_in(self, room) -> None:
        ...
    @abstractmethod
    def check_out(self, room) -> None:
        ...
    @abstractmethod
    def start_maintenance(self, room) -> None:
        ...
    @abstractmethod
    def end_maintenance(self, room) -> None:
        ...
    @abstractmethod
    def finish_cleaning(self, room) -> None:
        ...
    @abstractmethod
    def get_current(self) -> str:
        ...
    @abstractmethod
    def __str__(self) -> str:
        ...

#classes concretas dos estados

class Available(State):
    def book(self, room) -> None:
        room.estado.set_estado(Reserved())
     
    def check_in(self, room) -> None:
        room.estado.set_estado(Ocupied())
     
    def check_out(self, room) -> None:
        raise TypeError ("Quarto Desocupado")
     
    def start_maintenance(self, room) -> None:
        room.estado.set_estado(Maintenance())
     
    def end_maintenance(self, room) -> None:
        raise TypeError ("Quarto Não está em Manutenção")
     
    def finish_cleaning(self, room) -> None:
        raise TypeError ("Quarto já esta Limpo")
     
    def get_current(self) -> str:
        return "Disponível"
    
    def __str__(self) -> str:
        return "disponivel"
    
class Reserved(State):
    def book(self, room) -> None:
        raise TypeError ("Quarto ja está reservado")
        
    def check_in(self, room) -> None:
        room.estado.set_estado(Ocupied())
        
    def check_out(self, room) -> None:
        raise TypeError ("Quarto está Reservado")
        
    def start_maintenance(self, room) -> None:
        raise TypeError ("Quarto está Reservado, troque o hóspede de quarto") # ver possibilidade de implementar troca automatica
        
    def end_maintenance(self, room) -> None:
        raise TypeError ("Quarto está Reservado")
        
    def finish_cleaning(self, room) -> None:
        raise TypeError ("Quarto está Reservado")
        
    def get_current(self) -> str:
        return "Reservado"
    
    def __str__(self) -> str:
            return "reservado"

class Ocupied(State):
    def book(self, room) -> None:
        raise TypeError ("Quarto está Ocupado")
        
    def check_in(self, room) -> None:
        raise TypeError ("Quarto está Ocupado")
        
    def check_out(self, room) -> None:
        room.estado.set_estado(Cleaning())
        
    def start_maintenance(self, room) -> None:
        raise TypeError ("Quarto está Ocupado")
        
    def end_maintenance(self, room) -> None:
        raise TypeError ("Quarto está Ocupado")
        
    def finish_cleaning(self, room) -> None:
        raise TypeError ("Quarto está Ocupado")
        
    def get_current(self) -> str:
        return "Ocupado"
    
    def __str__(self) -> str:
            return "ocupado"
    
class Cleaning(State):
    def book(self, room) -> None:
        raise TypeError ("Quarto está em Limpeza")
        
    def check_in(self, room) -> None:
        raise TypeError ("Quarto está em Limpeza")
        
    def check_out(self, room) -> None:
        raise TypeError ("Quarto está em Limpeza")
        
    def start_maintenance(self, room) -> None:
        room.estado.set_estado(Maintenance())
        
    def end_maintenance(self, room) -> None:
        raise TypeError ("Quarto não está em Manutenção")
        
    def finish_cleaning(self, room) -> None:
        room.estado.set_estado(Available())
        
    def get_current(self) -> str:
        return "Em Limpeza"
    
    def __str__(self) -> str:
            return "limpeza"

class Maintenance(State):
    def book(self, room) -> None:
        raise TypeError ("Quarto está em Manutenção")
        
    def check_in(self, room) -> None:
        raise TypeError ("Quarto está em Manutenção")
        
    def check_out(self, room) -> None:
        raise TypeError ("Quarto está em Manutenção")
        
    def start_maintenance(self, room) -> None:
        raise TypeError ("Quarto está em Manutenção")
    
    def end_maintenance(self, room) -> None:
        room.estado.set_estado(Cleaning())
        
    def finish_cleaning(self, room) -> None:
        raise TypeError ("Quarto está em Manutenção")
        
    def get_current(self) -> str:
        return "Em Manutenção"
    
    def __str__(self) -> str:
            return "manutencao"