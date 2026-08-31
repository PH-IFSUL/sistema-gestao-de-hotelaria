from abc import ABC, abstractmethod

class Estado_Contexto:
    '''
    classe que serve de interface entre os estados da estadia do
    Hospede.
    '''
    _state = None

    def __init__(self, state: State) -> None:
        self._transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.Estado_Contexto = self


    def set_estado(self, novo_estado):
        # usado para definir novo estado
        self._estado_atual = novo_estado

    def get_nome(self):
        return self._estado_atual.get_nome()

class State(ABC):
    @abstractmethod
    def iniciar(self, estadia):
        pass


#classes concretas de estados

class Reservada(State):
    def iniciar(self, estadia):
            pass
    