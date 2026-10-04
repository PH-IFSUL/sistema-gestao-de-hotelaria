'''
    interface com qualquer tipo de Repo (Memória, sql, csv) para o cliente:
    
        -> todas as implementações tem que ter os mesmos métodos
'''
from typing import Protocol, List, Optional
from ...client.client import Client


class Client_Repository(Protocol):
    '''
    Métodos:
        save(cliente: Client) -> None:
        delete(client_cpf: str) -> bool:
        get_all() -> List[Client]:
        find_by_id(id_query: int) -> Optional[Client]:
        find_by_Cpf(cpf_query: str) -> Optional[Client]:
    '''

    def save(self, cliente: Client) -> None:
        '''
            Adiciona um cliente ao repositório.
        '''
        ...

    # @ fix -> remover por id
    def delete(self, client_cpf: str) -> bool:
        '''
            Remove um cliente do repositório pelo CPF.
        '''
        ...

    def get_all(self) -> List[Client]:
        '''
            Retorna todos os clientes do repositório.
        '''
        ...

    def find_by_id(self, id_query: int) -> Optional[Client]:
        '''
            Busca um cliente pelo ID.
        '''
        ...

    def find_by_Cpf(self, cpf_query: str) -> Optional[Client]:
        '''
            Busca um cliente pelo CPF.
        '''
        ...
        
    def update(self, guest: Client) -> bool:
        '''
            Atualiza um cliente no repositório.
        '''
        ...
