from models.database.connection import Database_Connection
from models.database.repositories.client_sqlite_repository import SQLite_Client_Repository
from models.database.repositories.room_sqlite_repository import SQLite_Room_Repository
from controllers.room_controller import Room_Controller
from controllers.client_controller import Client_Controller
from controllers.stay_controller import Stay_Controller
from views.main import JanelaPrincipal


def main():
    '''
    selecionar repositórios (aqui manda a implementação escolhida, não o protocolo(interface) dele).
    Se as classes estiverem iguais, então ele deve aceitar a implementação.
    '''
    banco = Database_Connection()  
    conexao = banco.get_connection()
    repo_clientes = SQLite_Client_Repository(conexao)
    repo_quartos  = SQLite_Room_Repository(conexao)

    '''
    controller recebe o repositório escolhido.
    '''
    ctrl_clientes = Client_Controller(repo_clientes) 
    ctrl_quartos  = Room_Controller(repo_quartos)
    stay_ctrl     = Stay_Controller(room_repo=repo_quartos, client_repo=repo_clientes)

    app = JanelaPrincipal(ctrl_clientes, ctrl_quartos, stay_ctrl) # janela principal recebe os controllers
    try:
        app.mainloop()
    finally:
        banco.close()


if __name__ == "__main__":
    main()