from models.room.room import Room
from models.database.interfaces.room_repository_interface import Room_Repository

class Room_Controller:
    '''
        Classe para gerenciar os quartos.
        
        Args:
            repo: repositorio de quartos
        
        Returns:
            Objeto do tipo Room_Controller.
    '''
    
    def __init__(self, repo: Room_Repository):
        self._repo = repo

    def cadastrar(self, 
                  numero_str: str,
                  tipo: str,
                  valor_str: str) -> str:
        """
        Cadastra um novo quarto.
        
        Args:
            numero_str: número do quarto
            tipo: tipo do quarto
            valor_str: valor da diária do quarto
        
        Returns:
            String informando que o quarto foi cadastrado com sucesso.
        """
        numero_str = numero_str.strip()
        valor_str = valor_str.strip().replace(",", ".")

        if not numero_str:
            raise ValueError("O campo Número é obrigatório.")
        if not numero_str.isdigit():
            raise ValueError("Número do quarto deve ser um valor inteiro.")
        if not tipo:
            raise ValueError("Selecione um tipo de quarto.")
        if not valor_str:
            raise ValueError("O campo Valor da Diária é obrigatório.")

        try:
            valor = float(valor_str)
        except ValueError:
            raise ValueError("Valor da diária deve ser um número "
                             "(ex: 150.00).")

        if valor <= 0:
            raise ValueError("Valor da diária deve ser maior que zero.")

        quarto = Room(int(numero_str), tipo, valor)
        self._repo.add(quarto)
        return f"Quarto {numero_str} ({tipo}) cadastrado com sucesso."

    def listar(self) -> list[Room]:
        """
        Lista todos os quartos.
        
        Returns:
            Lista de quartos.
        """
        return self._repo.list()

    def remover(self, numero_str: str) -> str:
        """
        Remove um quarto.
        
        Args:
            numero_str: número do quarto
        
        Returns:
            String informando que o quarto foi removido com sucesso.
        """
        numero_str = numero_str.strip()
        if not numero_str.isdigit():
            raise ValueError("Informe um número de quarto válido.")
        if not self._repo.delete(int(numero_str)):
            raise ValueError(f"Nenhum quarto encontrado com número "
                             f" {numero_str}.")
        return f"Quarto {numero_str} removido."

    def get_state_name(self, room: Room):
        """
        Obtém o nome do estado do quarto.
        
        Args:
            room: quarto
        
        Returns:
            Nome do estado do quarto.
        """
        return room.estado.get_current()
    
    def get_state_tag(self, room: Room):
        """
        Obtém a tag do estado do quarto.
        
        Args:
            room: quarto
        
        Returns:
            Tag do estado do quarto.
        """
        return room.estado.__str__()